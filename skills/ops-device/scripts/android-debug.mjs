#!/usr/bin/env bun
/** Android device evidence and bounded plans. No shell evaluation or implicit device selection. */
import {spawn} from 'node:child_process';
import {mkdir,writeFile,readFile,lstat,realpath,chmod} from 'node:fs/promises';
import {existsSync} from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {createHash,randomUUID} from 'node:crypto';
import {inflateSync} from 'node:zlib';

export const HELP=`Android Debug — Bun 1.4+, no dependencies
  bun android-debug.mjs devices [--adb /path/adb]
  bun android-debug.mjs collect --serial SERIAL --kind phone|emulator --out NEW_DIR [--package PKG]
  bun android-debug.mjs run --serial SERIAL --kind phone|emulator --out NEW_DIR --plan PLAN.json --allow-input
  bun android-debug.mjs record --serial SERIAL --kind phone|emulator --out NEW_DIR --seconds 1..30
  bun android-debug.mjs emulator-list [--emulator /path/emulator]
  bun android-debug.mjs emulator-start --avd NAME --port EVEN_PORT --out NEW_DIR --allow-start
Options: --adb PATH, --emulator PATH, --timeout 1000..60000 (per device command, default 15000).
Output is private evidence, not an automatic business pass. Output directory must not exist.
run plan: {schemaVersion:1, expectedPackage:'com.example.app', steps:[
 {op:'tap', selector:{resourceId:'download',text:'Download'}, expectPackage:'com.example.store'},
 {op:'back', expectPackage:'com.example.app'}]}
Allowed steps: tap (exact selector; one match), back, swipe (coordinates), launch (component),
open-url (https URL + browserPackage), wait (milliseconds 0..5000).
Each mutating step requires expectPackage. An action failure stops subsequent steps.
No install, unlock, app-data clearing, arbitrary shell, CDP, shared-log clearing or server reset.
record runs only bounded screen recording; does not inject input. Review captured pixels separately.
`;
const hash=b=>createHash('sha256').update(b).digest('hex');
export function crc32(b){let crc=0xffffffff;for(const v of b){crc^=v;for(let i=0;i<8;i++)crc=(crc>>>1)^((crc&1)?0xedb88320:0)}return (crc^0xffffffff)>>>0}
const now=()=>new Date().toISOString();
export const quoteShell=s=>"'"+String(s).replaceAll("'","'\\''")+"'";
export const deviceArgs=args=>args[0]==='shell'?['shell',args.slice(1).map(quoteShell).join(' ')]:args;
const pkg=s=>typeof s==='string'&&/^[A-Za-z][\w]*(?:\.[A-Za-z][\w]*)+$/.test(s);
function check(ok,message){if(!ok)throw new Error(message)}
function num(v,min,max,name){const n=Number(v);check(Number.isInteger(n)&&n>=min&&n<=max,`Invalid ${name}`);return n}
export function parseArgs(args){
 const [command,...rest]=args, o={command};
 const values=new Set(['adb','emulator','serial','kind','out','package','plan','seconds','avd','port','timeout']);
 for(let i=0;i<rest.length;i++){
  const k=rest[i].replace(/^--/,'');check(rest[i].startsWith('--')&&!(k in o),`Invalid/duplicate option ${rest[i]}`);
  if(['allow-input','allow-start'].includes(k))o[k]=true;
  else{check(values.has(k)&&rest[i+1]&&!rest[i+1].startsWith('--'),`Unknown/missing option ${rest[i]}`);o[k]=rest[++i]}
 }
 const options={devices:['adb','timeout'],'emulator-list':['emulator','timeout'],'emulator-start':['adb','emulator','avd','port','out','allow-start','timeout'],collect:['adb','timeout','serial','kind','out','package'],run:['adb','timeout','serial','kind','out','plan','allow-input'],record:['adb','timeout','serial','kind','out','seconds']};
 if(options[command])for(const k of Object.keys(o).filter(k=>k!=='command'))check(options[command].includes(k),`Option --${k} is not supported by ${command}`);
 if(o.timeout!==undefined)num(o.timeout,1000,60000,'timeout');return o;
}
export function parseDevices(s){return s.split(/\r?\n/).flatMap(line=>{
 if(!line.trim()||line.startsWith('List of devices attached')||line.startsWith('*'))return [];
 const m=line.match(/^(\S+)\s+(no permissions|\S+)(?:\s|$)(.*)/);
 return m?[{serial:m[1],state:m[2],details:m[3].trim(),kind:m[1].startsWith('emulator-')?'emulator':'phone'}]:[];
})}
export function foreground(s){const packages=new Set([...s.matchAll(/(?:topResumedActivity|mResumedActivity)[^\n]*?\s([\w.]+)\/([\w.$]+)/g)].map(m=>m[1]));return packages.size===1?[...packages][0]:null}
function xmlDecode(s){return s.replace(/&#(x[\da-f]+|\d+);|&(quot|apos|lt|gt|amp);/gi,(_,n,v)=>n?String.fromCodePoint(n[0].toLowerCase()==='x'?parseInt(n.slice(1),16):+n):({quot:'"',apos:"'",lt:'<',gt:'>',amp:'&'}[v]));}
export function nodes(xml){check(xml.includes('<hierarchy')&&xml.includes('</hierarchy>'),'Incomplete UI hierarchy');return [...xml.matchAll(/<node\b([^>]+)>/g)].map(m=>Object.fromEntries([...m[1].matchAll(/([\w-]+)="([^"]*)"/g)].map(a=>[a[1],xmlDecode(a[2])])))}
export function selectTarget(xml,selector){
 check(selector&&typeof selector==='object'&&!Array.isArray(selector),'Missing exact selector');
 const mapping={resourceId:'resource-id',text:'text',description:'content-desc'};
 const keys=Object.keys(selector);check(keys.length>0&&keys.every(k=>mapping[k]&&typeof selector[k]==='string'&&selector[k]),'Invalid selector');
 const matches=nodes(xml).filter(n=>keys.every(k=>n[mapping[k]]===selector[k])&&n.enabled==='true'&&n.clickable==='true');
 check(matches.length===1,`Selector must match exactly one enabled clickable node; found ${matches.length}`);
 const m=matches[0].bounds?.match(/^\[(\d+),(\d+)\]\[(\d+),(\d+)\]$/);check(m,'Invalid node bounds');
 const [x1,y1,x2,y2]=m.slice(1).map(Number);check(x2>x1&&y2>y1,'Empty node bounds');return {x:Math.floor((x1+x2)/2),y:Math.floor((y1+y2)/2),node:matches[0]};
}
export function validatePlan(p){
 check(p?.schemaVersion===1&&pkg(p.expectedPackage)&&Array.isArray(p.steps)&&p.steps.length>0&&p.steps.length<=20,'Invalid plan envelope');
 for(const s of p.steps){
  check(['tap','back','swipe','launch','open-url','wait'].includes(s.op),`Unsupported op ${s.op}`);
  if(s.op==='wait'){num(s.milliseconds,0,5000,'wait');continue}
  check(pkg(s.expectPackage),'Each action needs expectPackage');
  if(s.op==='tap'){check(s.selector&&Object.keys(s.selector).length,'Tap requires selector');for(const [k,v]of Object.entries(s.selector))check(['resourceId','text','description'].includes(k)&&typeof v==='string'&&v,'Invalid selector')}
  if(s.op==='swipe'){check(Array.isArray(s.from)&&Array.isArray(s.to)&&s.from.length===2&&s.to.length===2,'Invalid swipe');for(const v of [...s.from,...s.to])num(v,0,20000,'coordinate');num(s.durationMs??300,50,2000,'swipe duration')}
  if(s.op==='launch')check(typeof s.component==='string'&&/^[\w.]+\/[\w.$]+$/.test(s.component)&&s.component.split('/')[0]===s.expectPackage,'Invalid component or expected package');
  if(s.op==='open-url'){let u;try{u=new URL(s.url)}catch{}check(u?.protocol==='https:'&&!u.username&&!u.password&&pkg(s.browserPackage),'Only HTTPS URL with explicit browserPackage is supported');}
 }
 return p;
}
export function validatePng(b){
 check(b.length>=45&&b.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])),'Invalid PNG signature');
 let pos=8,width=0,height=0,idat=[],ended=false,channels=0;
 while(pos+12<=b.length){const len=b.readUInt32BE(pos),type=b.toString('ascii',pos+4,pos+8);check(len<=64*1024*1024&&pos+12+len<=b.length,'Truncated PNG');check(crc32(b.subarray(pos+4,pos+8+len))===b.readUInt32BE(pos+8+len),'PNG CRC mismatch');const data=b.subarray(pos+8,pos+8+len);
  if(type==='IHDR'){check(pos===8&&len===13,'Invalid PNG header');width=data.readUInt32BE(0);height=data.readUInt32BE(4);channels=({0:1,2:3,4:2,6:4})[data[9]];check(width>0&&height>0&&width<=16384&&height<=16384&&data[8]===8&&channels&&data[12]===0,'Unsupported PNG layout');}
  if(type==='IDAT')idat.push(data);pos+=12+len;if(type==='IEND'){ended=true;break}
 }
 check(ended&&pos===b.length&&idat.length&&width>0&&height>0&&channels,'Incomplete PNG');const size=(width*channels+1)*height;check(size<=128*1024*1024,'PNG decoded size too large');
 const decoded=inflateSync(Buffer.concat(idat),{maxOutputLength:size});check(decoded.length===size,'Invalid PNG image data');return {width,height,sha256:hash(b)};
}
function findTool(explicit,name){
 if(explicit){check(path.isAbsolute(explicit)&&existsSync(explicit),`Invalid ${name} path`);return explicit}
 const candidates=(process.env.PATH||'').split(path.delimiter).map(p=>path.join(p,name));
 for(const root of [process.env.ANDROID_SDK_ROOT,process.env.ANDROID_HOME,path.join(os.homedir(),'Library/Android/sdk')].filter(Boolean))candidates.push(path.join(root,name==='adb'?'platform-tools':'emulator',name));
 const found=candidates.find(p=>existsSync(p));check(found,`${name} not found in PATH and configured/default SDK locations`);return found;
}
async function exec(file,args,{timeout=15000,maxBytes=16*1024*1024}={}){
 return await new Promise(resolve=>{let chunks=[],errors=[],size=0,errorSize=0,reason=null;
  const p=spawn(file,args,{stdio:['ignore','pipe','pipe']});const timer=setTimeout(()=>{reason='timeout';p.kill('SIGKILL')},timeout);
  p.stdout.on('data',c=>{size+=c.length;if(size>maxBytes){reason='output-limit';p.kill('SIGKILL')}else chunks.push(c)});
  p.stderr.on('data',c=>{errorSize+=c.length;if(errorSize<=65536)errors.push(c)});
  p.on('error',e=>{reason=e.message});p.on('close',(code,signal)=>{clearTimeout(timer);resolve({code,signal,reason,stdout:Buffer.concat(chunks),stderr:Buffer.concat(errors).toString()})});
 });
}
async function privateFile(p,b){await writeFile(p,b,{mode:0o600,flag:'wx'})}
async function newOutput(p){check(p&&path.isAbsolute(p),'--out must be an absolute new directory');await mkdir(p,{mode:0o700});check(!(await lstat(p)).isSymbolicLink(),'Output cannot be symlink');return await realpath(p)}
async function hostLock(){if(process.platform!=='darwin')return 'unknown';const r=await exec('/usr/sbin/ioreg',['-n','Root','-d1'],{maxBytes:1024*1024});return r.stdout.toString().match(/"IOConsoleLocked"\s*=\s*(Yes|No)/)?.[1]||'unknown'}
async function session(o){
 check(o.serial&&/^[\w.:-]+$/.test(o.serial),'Explicit --serial required');check(['phone','emulator'].includes(o.kind),'--kind phone|emulator required');if(o.package)check(pkg(o.package),'Invalid package');
 const adb=findTool(o.adb,'adb'),timeout=num(o.timeout??15000,1000,60000,'timeout');
 const list=await exec(adb,['devices','-l'],{timeout});check(list.code===0&&!list.reason,'Device inventory failed');const d=parseDevices(list.stdout.toString()).find(x=>x.serial===o.serial);check(d&&d.state==='device',`Requested device unavailable (${d?.state||'not listed'})`);check(d.kind===o.kind,'Device kind mismatch');
 const out=await newOutput(o.out),manifest={schemaVersion:1,id:randomUUID(),startedAt:now(),adb,device:d,hostLockBefore:await hostLock(),commands:[],captures:[],steps:[],cleanup:[],claim:'evidence-only; visual and business acceptance require review'};
 async function save(){await writeFile(path.join(out,'manifest.json'),JSON.stringify(manifest,null,2),{mode:0o600})}
 async function run(args,maxBytes,commandTimeout=timeout){const entry={at:now(),args,state:'invoking',code:null,timeoutMs:commandTimeout};manifest.commands.push(entry);await save();const r=await exec(adb,['-s',o.serial,...deviceArgs(args)],{timeout:commandTimeout,maxBytes});Object.assign(entry,{finishedAt:now(),state:'terminal',code:r.code,signal:r.signal,reason:r.reason,stderr:r.stderr});await save();return r}
 async function required(args,maxBytes){const r=await run(args,maxBytes);check(r.code===0&&!r.reason,`ADB failed: ${args.slice(0,3).join(' ')} (${r.reason||r.code})`);return r.stdout}
 async function activity(){return (await required(['shell','dumpsys','activity','activities'])).toString()}
 async function guard(expected){const text=await activity();check(foreground(text)===expected,`Foreground package mismatch: expected ${expected}; found ${foreground(text)}`);
  const w=(await required(['shell','dumpsys','window','policy'])).toString();const locks=[...w.matchAll(/^\s*(?:showing|mKeyguardShowing|KeyguardShowing|mIsShowing)=(true|false)/gm)];check(locks.length>0&&locks.every(m=>m[1]==='false'),'Phone/guest unlock state not verified');
 }
 async function capture(label){
  const start=now(),base=path.join(out,label);const a=await activity();await privateFile(base+'.activity.txt',a);
  const png=await required(['exec-out','screencap','-p'],32*1024*1024);await privateFile(base+'.png',png);const image=validatePng(png);
  const guest=`/sdcard/ops-client-${manifest.id}-${label}.xml`;let xml=null,dumpCompleted=false;
  try{await required(['shell','uiautomator','dump',guest]);dumpCompleted=true;xml=(await required(['shell','cat',guest])).toString();nodes(xml);await privateFile(base+'.xml',xml)}catch(e){xml=null;manifest.captures.push({label,uiError:e.message});}
  finally{const r=await run(['shell','rm',guest]);const removed=r.code===0&&!r.reason;manifest.cleanup.push({guest,removed:removed?true:null,status:removed?'removed':dumpCompleted?'removal-unverified':'creation-and-removal-unverified'})}
  manifest.captures.push({label,startedAt:start,at:now(),package:foreground(a),image,xml:xml!==null});await save();return {xml,image,package:foreground(a)};
 }
 async function finish(error){manifest.finishedAt=now();manifest.hostLockAfter=await hostLock();manifest.status=error?'failed':'completed';if(error)manifest.error=error.message;await save();console.log(JSON.stringify({status:manifest.status,out,device:d.serial,error:error?.message}));}
 return {adb,out,manifest,run,required,activity,guard,capture,finish,save,timeout};
}
async function collect(s,o){
 const props=(await s.required(['shell','getprop'])).toString().split('\n').filter(x=>/\[(ro.product.(model|brand|device|cpu.abi)|ro.build.version.(sdk|release)|sys.boot_completed)\]/.test(x));
 await privateFile(path.join(s.out,'device.txt'),props.join('\n'));
 if(o.package)await privateFile(path.join(s.out,'package.txt'),await s.required(['shell','dumpsys','package',o.package]));
 await s.capture('before');
 const logs=await s.run(['logcat','-d','-v','threadtime','-t','300','ActivityTaskManager:I','ActivityManager:I','*:S']);await privateFile(path.join(s.out,'activities.log'),logs.stdout);
}
async function runPlan(s,o,plan){
 check(o['allow-input'],'--allow-input required');validatePlan(plan);await privateFile(path.join(s.out,'plan.json'),JSON.stringify(plan,null,2));
 let expected=plan.expectedPackage;await s.guard(expected);let before=await s.capture('before');
 for(let i=0;i<plan.steps.length;i++){
  const step=plan.steps[i];await s.guard(expected);const record={index:i,step,startedAt:now(),status:'not-executed'};s.manifest.steps.push(record);
  if(step.op==='wait')await new Promise(r=>setTimeout(r,step.milliseconds));
  else{
   let args;
   if(step.op==='tap'){
    // Hierarchy is refreshed at this action boundary rather than using a previous step's image.
    before=await s.capture(`pre-${i}`);check(before.xml,'Tap requires current hierarchy');const t=selectTarget(before.xml,step.selector);check(t.x<before.image.width&&t.y<before.image.height,'Tap outside image');record.target={x:t.x,y:t.y,bounds:t.node.bounds};args=['shell','input','tap',String(t.x),String(t.y)];
   }else if(step.op==='back')args=['shell','input','keyevent','4'];
   else if(step.op==='swipe'){
    before=await s.capture(`pre-${i}`);check([...step.from,...step.to].every((n,j)=>n<(j%2?before.image.height:before.image.width)),'Swipe outside image');args=['shell','input','swipe',...step.from.map(String),...step.to.map(String),String(step.durationMs??300)];
   }else if(step.op==='launch')args=['shell','am','start','-W','-n',step.component];
   else args=['shell','am','start','-W','-a','android.intent.action.VIEW','-d',step.url,'-p',step.browserPackage];
   await s.guard(expected);record.status='attempted';await s.save();await s.required(args);expected=step.expectPackage;
  }
  const until=Date.now()+5000;while(Date.now()<until){if(foreground(await s.activity())===expected)break;await new Promise(r=>setTimeout(r,250))}
  const after=await s.capture(`after-${i}`);check(after.package===expected,`Step ${i} destination mismatch`);record.status=step.op==='wait'?'valid-noop':'observed-package';record.finishedAt=now();
 }
 const logs=await s.run(['logcat','-d','-v','threadtime','-t','500','ActivityTaskManager:I','ActivityManager:I','*:S']);await privateFile(path.join(s.out,'activities.log'),logs.stdout);
}
async function recordScreen(s,o){
 const seconds=num(o.seconds,1,30,'record seconds'),guest=`/sdcard/ops-client-${s.manifest.id}.mp4`;
 const probe=await s.run(['shell','screenrecord','--help']);check(probe.code===0&&!probe.reason&&(probe.stdout.toString()+probe.stderr).includes('--time-limit'),'screenrecord time-limit unavailable');await s.capture('before');
 s.manifest.recording={guest,secondsRequested:seconds,state:'invoking',startedAt:now(),validation:'requires external codec/duration/frame review'};await s.save();let pulled=false;
 try{const r=await s.run(['shell','screenrecord','--time-limit',String(seconds),guest],undefined,(seconds+10)*1000);Object.assign(s.manifest.recording,{state:'terminal',finishedAt:now(),code:r.code,reason:r.reason});await s.save();check(r.code===0&&!r.reason,'Recording failed');await s.required(['pull',guest,path.join(s.out,'screen.mp4')]);await chmod(path.join(s.out,'screen.mp4'),0o600);check((await lstat(path.join(s.out,'screen.mp4'))).size>0,'Empty recording');pulled=true;}
 finally{if(pulled){const r=await s.run(['shell','rm',guest]);s.manifest.cleanup.push({guest,removed:r.code===0&&!r.reason})}else{s.manifest.cleanup.push({guest,removed:false,retained:true,reason:'recording-or-transfer-failed; reconcile-original-before-cleanup'})}}
 await s.capture('after');
}
async function emulatorStart(o){
 check(o['allow-start'],'--allow-start required');check(o.avd&&/^[\w.-]+$/.test(o.avd),'Invalid AVD');const port=num(o.port,5554,5682,'port');check(port%2===0,'Emulator port must be even');
 const emulator=findTool(o.emulator,'emulator'),adb=findTool(o.adb,'adb'),timeout=num(o.timeout??15000,1000,60000,'timeout');const inventory=await exec(adb,['devices','-l'],{timeout});check(inventory.code===0&&!inventory.reason,'Device inventory failed');check(!parseDevices(inventory.stdout.toString()).some(d=>d.serial===`emulator-${port}`),'ADB serial already in use');
 for(const d of parseDevices(inventory.stdout.toString()).filter(d=>d.kind==='emulator')){
  check(d.state==='device','Cannot establish existing emulator ownership while offline');
  const r=await exec(adb,['-s',d.serial,'emu','avd','name'],{timeout});check(r.code===0&&!r.reason,'Cannot read existing emulator AVD');check(r.stdout.toString().split(/\r?\n/)[0].trim()!==o.avd,'Requested AVD already running on another serial');
 }
 const net=await import('node:net');for(const p of [port,port+1])await new Promise((resolve,reject)=>{const server=net.createServer();server.once('error',()=>reject(new Error(`Emulator port ${p} is occupied`)));server.listen(p,'127.0.0.1',()=>server.close(resolve))});
 const avds=await exec(emulator,['-list-avds'],{timeout});check(avds.code===0&&!avds.reason&&avds.stdout.toString().split(/\r?\n/).includes(o.avd),'AVD not found');
 // Vendor handles image/ABI/acceleration validation; failure evidence is retained.
 const out=await newOutput(o.out);const {open}=await import('node:fs/promises');const log=await open(path.join(out,'emulator.log'),'wx',0o600);
 const receipt={id:randomUUID(),startedAt:now(),avd:o.avd,serial:`emulator-${port}`,pid:null,executable:emulator,ownership:'launch-intent-only-until-pid-bound',status:'invoking'};await privateFile(path.join(out,'launch.json'),JSON.stringify(receipt,null,2));
 const child=spawn(emulator,['-avd',o.avd,'-port',String(port),'-no-window','-no-snapshot-save'],{stdio:['ignore',log.fd,log.fd]});let exited=false;child.on('exit',()=>{exited=true});child.on('error',e=>{exited=true;receipt.spawnError=e.message});await log.close();receipt.pid=child.pid??null;receipt.status='starting';receipt.ownership=child.pid?'started-by-this-invocation':'launch-not-confirmed';await writeFile(path.join(out,'launch.json'),JSON.stringify(receipt,null,2),{mode:0o600});
 const until=Date.now()+90000;let ready=false;
 while(Date.now()<until&&!exited){const r=await exec(adb,['-s',receipt.serial,'shell','getprop','sys.boot_completed'],{timeout:Math.min(4000,timeout)});if(r.code===0&&r.stdout.toString().trim()==='1'){const a=await exec(adb,['-s',receipt.serial,'shell','dumpsys','activity','activities'],{timeout:Math.min(4000,timeout)});if(foreground(a.stdout.toString())){ready=true;break}}await new Promise(r=>setTimeout(r,1000))}
 receipt.status=ready?'booted':'not-verified';receipt.finishedAt=now();await writeFile(path.join(out,'launch.json'),JSON.stringify(receipt,null,2),{mode:0o600});child.unref();console.log(JSON.stringify({...receipt,out,retained:true}));if(!ready)process.exitCode=1;
}
export async function main(args){
 const o=parseArgs(args);if(!o.command||['--help','help'].includes(o.command)){console.log(HELP);return}
 check(['devices','collect','run','record','emulator-list','emulator-start'].includes(o.command),'Unknown command; use --help');
 if(o.command==='devices'||o.command==='emulator-list'){
  const file=findTool(o.command==='devices'?o.adb:o.emulator,o.command==='devices'?'adb':'emulator');const r=await exec(file,o.command==='devices'?['devices','-l']:['-list-avds'],{timeout:num(o.timeout??15000,1000,60000,'timeout')});check(r.code===0&&!r.reason,'Inventory failed');console.log(JSON.stringify(o.command==='devices'?parseDevices(r.stdout.toString()):r.stdout.toString().trim().split(/\r?\n/).filter(Boolean),null,2));return;
 }
 if(o.command==='emulator-start'){await emulatorStart(o);return}
 let plan;if(o.command==='run'){check(o['allow-input']&&o.plan,'run requires --allow-input and --plan');plan=validatePlan(JSON.parse(await readFile(o.plan,'utf8')))}
 if(o.command==='record')num(o.seconds,1,30,'record seconds');
 const s=await session(o);try{if(o.command==='collect')await collect(s,o);else if(o.command==='run')await runPlan(s,o,plan);else await recordScreen(s,o);await s.finish()}catch(e){await s.finish(e);process.exitCode=1}
}
if(import.meta.main)main(process.argv.slice(2)).catch(e=>{console.error(JSON.stringify({status:'failed',error:e.message,actionState:'inspect-owned-manifest-or-launch-receipt; do not infer not-executed'}));process.exitCode=1});

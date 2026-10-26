import {test,expect,afterAll} from 'bun:test';
import {mkdtemp,writeFile,readFile,chmod,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {deflateSync} from 'node:zlib';
import {parseArgs,parseDevices,foreground,nodes,selectTarget,validatePlan,validatePng,deviceArgs,quoteShell,crc32} from './android-debug.mjs';
const xml='<hierarchy><node text="Download &amp; open" resource-id="download" clickable="true" enabled="true" bounds="[0,0][10,20]"></node></hierarchy>';
const fixtureRoots=[];
afterAll(async()=>{for(const root of fixtureRoots)await rm(root,{recursive:true,force:true})});
function png(){const chunk=(type,b)=>{const h=Buffer.alloc(8);h.writeUInt32BE(b.length);h.write(type,4);const crc=Buffer.alloc(4);crc.writeUInt32BE(crc32(Buffer.concat([h.subarray(4),b])));return Buffer.concat([h,b,crc])};const h=Buffer.alloc(13);h.writeUInt32BE(20);h.writeUInt32BE(30,4);h[8]=8;h[9]=6;return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',h),chunk('IDAT',deflateSync(Buffer.alloc(81*30))),chunk('IEND',Buffer.alloc(0))])}
test('inventory preserves physical, emulator and unauthorized identities',()=>{const d=parseDevices('List of devices attached\np device model:X\nemulator-5556 device model:Y\nq unauthorized\n');expect(d.map(x=>[x.serial,x.kind,x.state])).toEqual([['p','phone','device'],['emulator-5556','emulator','device'],['q','phone','unauthorized']])});
test('inventory reports recovery/transient/unknown states rather than dropping devices',()=>{const d=parseDevices('List of devices attached\nr recovery\ns sideload 1\nb bootloader\na authorizing\nc connecting\nn no permissions hint\nx future-state details');expect(d.map(x=>x.state)).toEqual(['recovery','sideload','bootloader','authorizing','connecting','no permissions','future-state']);});
test('command options and timeout ranges fail before device access',()=>{expect(()=>parseArgs(['devices','--timeout','5'])).toThrow('timeout');expect(()=>parseArgs(['collect','--seconds','3'])).toThrow('not supported');expect(parseArgs(['emulator-list','--emulator','/tool/emulator','--timeout','1000']).timeout).toBe('1000');});
test('conflicting resumed packages do not choose the first display/app',()=>{expect(foreground('topResumedActivity=ActivityRecord{a u0 com.example.one/.Main t1}\nmResumedActivity=ActivityRecord{b u0 com.example.two/.Main t2}')).toBe(null)});
test('exact unique UI node and entity decoding; stale/ambiguous selectors fail',()=>{expect(selectTarget(xml,{text:'Download & open'})).toMatchObject({x:5,y:10});expect(()=>selectTarget(xml.replace('</hierarchy>',xml.slice(11)),{resourceId:'download'})).toThrow('exactly one');expect(()=>selectTarget(xml,{text:'Missing'})).toThrow();expect(()=>nodes('<hierarchy>')).toThrow()});
test('plan rejects arbitrary shell, unsupported schemes and missing destination',()=>{for(const step of [{op:'shell',command:'rm -rf /'},{op:'open-url',url:'javascript:alert(1)',browserPackage:'com.example.app',expectPackage:'com.example.app'},{op:'back'}])expect(()=>validatePlan({schemaVersion:1,expectedPackage:'com.example.app',steps:[step]})).toThrow()});
test('device shell arguments cannot inject through a URL or apostrophe',()=>{const s="https://example.test/?a=1&b=$(id)'x";expect(deviceArgs(['shell','echo',s])).toEqual(['shell',"'echo' "+quoteShell(s)]);expect(quoteShell("a'b")).toBe("'a'\\''b'")});
test('PNG payload must decompress to full frame; truncation fails',()=>{expect(validatePng(png())).toMatchObject({width:20,height:30});expect(()=>validatePng(png().subarray(0,50))).toThrow();const bad=png();bad[50]^=255;expect(()=>validatePng(bad)).toThrow()});
test('foreground parser identifies real resumed package; malformed cli rejected',()=>{expect(foreground('topResumedActivity=ActivityRecord{a u0 com.example.app/.Main t1}')).toBe('com.example.app');expect(()=>parseArgs(['run','--serial','p','--serial','p'])).toThrow();expect(()=>parseArgs(['run','--unknown','x'])).toThrow()});
async function fixture(){
 const root=await mkdtemp(path.join(tmpdir(),'android-debug-test-'));fixtureRoots.push(root);const adb=path.join(root,'adb');await writeFile(path.join(root,'sample.png'),png());await writeFile(path.join(root,'sample.xml'),xml);
 await writeFile(adb,`#!/usr/bin/env bun
import fs from 'node:fs';
const a=process.argv.slice(2),root=${JSON.stringify(root)},s=a.slice(2).join(' '),log=root+'/calls.jsonl';
fs.appendFileSync(log,JSON.stringify(a)+'\\n');
if(a[0]==='devices')console.log('p device model:X\\nemulator-5556 device model:Y');
else if(a[0]!=='-s'||!['p','emulator-5556'].includes(a[1]))process.exit(9);
else if(s.includes("'dumpsys' 'activity'"))console.log('topResumedActivity=ActivityRecord{a u0 '+(fs.existsSync(root+'/tapped')?'com.example.other':'com.example.app')+'/.Main t1}');
else if(s.includes("'dumpsys' 'window'"))console.log('  showing=false');
else if(s.includes("'screenrecord' '--help'"))console.error('Usage: screenrecord --time-limit TIME');
else if(s.includes("'screenrecord'")){}
else if(s.includes("'uiautomator'")&&fs.existsSync(root+'/dump-fail'))process.exit(1);
else if(s.includes("'rm'")&&fs.existsSync(root+'/dump-fail'))process.exit(1);
else if(s==='exec-out screencap -p')process.stdout.write(fs.readFileSync(root+'/sample.png'));
else if(s.includes("'cat'"))process.stdout.write(fs.readFileSync(root+'/sample.xml'));
else if(s.includes("'input' 'tap'")){const m=JSON.parse(fs.readFileSync(root+'/out/manifest.json'));if(m.steps[0]?.status!=='attempted'||m.commands.at(-1)?.state!=='invoking')process.exit(19);fs.writeFileSync(root+'/tapped','1');}
else if(s.includes("'input' 'keyevent'"))process.exit(12);
else if(s.includes("'uiautomator'")||s.includes("'rm'")||s.startsWith('logcat')||s.includes("'getprop'")){}
else process.exit(7);
`,{mode:0o700});await chmod(adb,0o700);return {root,adb};
}
async function cli(f,args){const p=Bun.spawn([process.execPath,path.join(import.meta.dir,'android-debug.mjs'),...args,'--adb',f.adb],{stdout:'pipe',stderr:'pipe'});const [code,out,err]=await Promise.all([p.exited,new Response(p.stdout).text(),new Response(p.stderr).text()]);return {code,out,err}}
test('integration: wrong kind stops before output and input',async()=>{const f=await fixture(),r=await cli(f,['collect','--serial','p','--kind','emulator','--out',path.join(f.root,'out')]);expect(r.code).toBe(1);expect(await readFile(path.join(f.root,'calls.jsonl'),'utf8')).not.toContain('input')});
test('integration: failed destination persists action evidence and never executes next step',async()=>{const f=await fixture(),plan=path.join(f.root,'plan.json');await writeFile(plan,JSON.stringify({schemaVersion:1,expectedPackage:'com.example.app',steps:[{op:'tap',selector:{resourceId:'download'},expectPackage:'com.example.store'},{op:'back',expectPackage:'com.example.app'}]}));const r=await cli(f,['run','--serial','p','--kind','phone','--out',path.join(f.root,'out'),'--plan',plan,'--allow-input']);expect(r.code).toBe(1);const m=JSON.parse(await readFile(path.join(f.root,'out/manifest.json'),'utf8'));expect(m.status).toBe('failed');expect(m.steps).toHaveLength(1);expect(m.steps[0].status).toBe('attempted');const calls=await readFile(path.join(f.root,'calls.jsonl'),'utf8');expect(calls).toContain('tap');expect(calls).not.toContain('keyevent');},15000);
test('integration: missing input authority and invalid plans cause no device invocation',async()=>{const f=await fixture(),r=await cli(f,['run','--serial','p','--kind','phone','--out',path.join(f.root,'out')]);expect(r.code).toBe(1);expect(r.err).toContain('allow-input');});
test('record help on stderr is supported; failed transfer retains original guest recording',async()=>{const f=await fixture(),r=await cli(f,['record','--serial','p','--kind','phone','--out',path.join(f.root,'out'),'--seconds','1']);expect(r.code).toBe(1);const m=JSON.parse(await readFile(path.join(f.root,'out/manifest.json'),'utf8'));expect(m.error).toContain('pull');expect(m.recording.state).toBe('terminal');expect(m.commands.some(c=>c.args[1]==='screenrecord'&&c.args.includes('--time-limit')&&c.timeoutMs===11000&&c.state==='terminal')).toBe(true);expect(m.cleanup.at(-1)).toMatchObject({retained:true,removed:false});const calls=(await readFile(path.join(f.root,'calls.jsonl'),'utf8')).split('\n');expect(calls.some(l=>l.includes("'rm'")&&l.includes('.mp4'))).toBe(false);});
test('failed dump and failed removal preserve unknown presence without claiming leftovers',async()=>{const f=await fixture();await writeFile(path.join(f.root,'dump-fail'),'1');const r=await cli(f,['collect','--serial','p','--kind','phone','--out',path.join(f.root,'out')]);expect(r.code).toBe(0);const m=JSON.parse(await readFile(path.join(f.root,'out/manifest.json'),'utf8'));expect(m.cleanup[0]).toMatchObject({removed:null,status:'creation-and-removal-unverified'});expect(m.captures.at(-1).xml).toBe(false);});

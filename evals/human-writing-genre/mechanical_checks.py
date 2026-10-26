"""Literal checks only. No model calls, factual inference, or writing-quality scores.
Import check_case(writer_case, oracle_case, output_text), or run on a JSON map id->output.
This file and the oracle file are review-side only, never writer context.
"""
import json, sys
from pathlib import Path

def check_case(case, oracle, output):
    results=[]
    for assertion in oracle['assertions']:
        mode=assertion.get('check_mode'); data=assertion.get('data')
        if mode=='equals_source_text':
            passed=output==case['source_text']; detail='exact Unicode equality; no normalization'
        elif mode=='exact_substring_count':
            actual=output.count(data['text']); passed=actual>=data['minimum_occurrences']
            detail={'found':actual,'minimum':data['minimum_occurrences'],'text':data['text']}
        elif mode=='immutable_prefix_suffix':
            prefix=data['immutable_prefix']; suffix=data['immutable_suffix']
            passed=output.startswith(prefix) and output.endswith(suffix)
            size=len(output)-len(prefix)-len(suffix)
            passed=passed and (size>0 if data['replacement_must_be_nonempty'] else size>=0)
            detail='prefix/suffix literal preservation only; replacement meaning and single-region scope still require review'
        else:
            continue
        results.append({'assertion_id':assertion['id'],'verdict':'pass' if passed else 'fail','detail':detail})
    return {'case_id':case['id'],'literal_checks':results,'semantic_review_required':True,'hard_gate':'not_determined_by_this_tool'}

if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python3 mechanical_checks.py output-map.json (JSON object id -> output text)')
    root=Path(__file__).resolve().parent
    cases={x['id']:x for n in ['development-inputs.json','holdout-inputs.json'] for x in json.loads((root/n).read_text())}
    oracles={x['id']:x for x in json.loads((root/'oracles.json').read_text())}
    outputs=json.loads(Path(sys.argv[1]).read_text())
    print(json.dumps([check_case(cases[id],oracles[id],out) for id,out in outputs.items()],ensure_ascii=False,indent=2))

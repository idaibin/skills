"""Validate the closed evaluation corpus; never grade prose quality."""
from pathlib import Path
from collections import Counter
import hashlib
import json
from jsonschema import Draft202012Validator

def main():
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'corpus.json').read_text())
    for name,digest in manifest['file_sha256'].items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Corpus drift: '+name)
    schema=json.loads((root/'writer-input.schema.json').read_text())
    cases=[a for name in ['development-inputs.json','holdout-inputs.json'] for a in json.loads((root/name).read_text())]
    oracles=json.loads((root/'oracles.json').read_text())
    assert len(cases)==96 and len({a['id'] for a in cases})==96
    assert len({a['source_text'] for a in cases})==96
    assert {a['id'] for a in cases}=={a['id'] for a in oracles}
    Draft202012Validator(schema).validate(cases)
    types={a['primary_type'] for a in cases}
    assert len(types)==8
    for typ in types:
        selected=[a for a in cases if a['primary_type']==typ]
        assert len(selected)==12
        assert Counter(a['split'] for a in selected)=={'development':10,'holdout':2}
        assert Counter(a['language'] for a in selected)=={'zh':8,'en':4}
        assert any(a['split']=='holdout' and a['length_profile']!='short' for a in selected)
    for oracle in oracles:
        ids=[a['id'] for a in oracle['assertions']]
        assert len(ids)==len(set(ids))
        assert all(d.get('applicability',{}).get('applies') in [True,False] for d in oracle['genre_oracles'])
        if oracle.get('review_mode')=='exact_noop_genre_not_applicable':
            assert all(not d['applicability']['applies'] for d in oracle['genre_oracles'])
    fresh=root/'fresh-holdout'
    extension=json.loads((fresh/'manifest.json').read_text())
    for name,digest in extension['file_sha256'].items():
        assert hashlib.sha256((fresh/name).read_bytes()).hexdigest()==digest, name
    extra=json.loads((fresh/'cases.json').read_text())
    extra_oracles=json.loads((fresh/'oracles.json').read_text())
    assert len(extra)==16 and {x['id'] for x in extra}=={x['id'] for x in extra_oracles}
    assert len({x['id'] for x in cases+extra})==112
    assert len({x['source_text'] for x in cases+extra})==112
    assert Counter(x['primary_type'] for x in extra)=={typ:2 for typ in types}
    assert all(Counter(x['language'] for x in extra if x['primary_type']==typ)=={'zh':1,'en':1} for typ in types)
    assert all('conditional_fidelity' in x for x in extra_oracles)
    print('96 original + 16 new held-out distinct inputs; 8 types x 14; frozen hashes valid. Semantic behavior is not determined.')

if __name__=='__main__':
    main()

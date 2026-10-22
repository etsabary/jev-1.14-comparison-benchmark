"""Offline public-bundle privacy and independent evidence checks."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

import assemble_corrected as a
import export_corrected as e
import validate_corrected_public as v


class PublicCorrection(unittest.TestCase):
    def test_privacy_guards_json_jsonl_paths_keys_and_per_item_correctness(self):
        for value in ({'user_id':'private'},{'gold_option':'1'},{'correct_first':True}):
            with self.assertRaises(AssertionError):v.privacy_guard(json.dumps(value).encode())
        text=json.dumps({'safe':1})+'\n'+json.dumps({'account_id':'private'})+'\n'
        with self.assertRaises(AssertionError):v.privacy_guard(text.encode())
        owner_path='/'+'Users/'+'example/private.txt'
        with self.assertRaises(AssertionError):v.privacy_guard(json.dumps({'path':owner_path}).encode())
        with self.assertRaises(AssertionError):v.privacy_guard(json.dumps({'token':'sk-'+'a'*30}).encode())
        v.privacy_guard(json.dumps({'key_name':'OPENROUTER_API_KEY','primary':{'correct':10}}).encode())

    def test_independent_money_matches_accounted_fallback_unknowns(self):
        rows=[{'reported_cost_usd':.1},{'reported_cost_usd':.2,'accounted_cost_usd':None},
              {'reported_cost_usd':None,'accounted_cost_usd':.3},{'reported_cost_usd':None}]
        self.assertEqual(v.money(rows),a.monetary(rows))
        self.assertEqual(v.money(rows,True),a.monetary(rows,True))

    def test_independent_quantiles_and_first_attempts(self):
        values=[1]*1134+[1000,1000]
        self.assertEqual(v.quantiles(values),{'n':1136,'median_ms':1.0,'p95_ms':1.0})
        self.assertEqual(v.firsts([{'item_id':'A','attempt':2,'value':'recovery'},{'item_id':'A','attempt':1,'value':'first'}])['A']['value'],'first')
        with self.assertRaises(AssertionError):v.firsts([{'item_id':'A','attempt':1}]*2)

    def test_source_map_must_stay_inside_root_and_match_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'archive').mkdir();path=root/'archive/attempts.jsonl';path.write_text('{}\n')
            self.assertEqual(v.checked_source(root,'old/attempts.jsonl',v.file_hash(path),{'old/attempts.jsonl':'archive/attempts.jsonl'}),path)
            with self.assertRaises(AssertionError):v.checked_source(root,'old/attempts.jsonl','wrong',{'old/attempts.jsonl':'archive/attempts.jsonl'})
            with self.assertRaises(AssertionError):v.checked_source(root,'old/attempts.jsonl','wrong',{'old/attempts.jsonl':'../outside'})

    def test_source_code_files_do_not_contain_owner_paths(self):
        for name in ('validate_corrected_public.py','export_corrected.py','assemble_corrected.py',
                     'test_assemble_corrected.py','test_export_corrected.py'):
            v.privacy_guard((a.ROOT/name).read_bytes())


if __name__=='__main__':unittest.main()

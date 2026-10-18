"""Offline correction-assembly regression tests; no inference or credentials."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

import assemble_corrected as a


class CorrectedAssembly(unittest.TestCase):
    def bank_fixture(self):
        old=[];metadata=[];keys={}
        for n in range(4):
            mid=f'O{n}';question=f'Old question{n}?'
            row={'item_id':mid,'instructions':'I','context':'C','question':question,'prompt_text':'I\n\nC\n\n'+question,
                 'prompt_sha256':f'oldhash{n}',**{f'option_{i}':f'Choice{i}' for i in range(1,6)}}
            old.append(row);metadata.append({'item_id':mid,'base_id':'O0' if n==2 else mid,'role':'core' if n<2 else 'robustness','prompt_sha256':row['prompt_sha256']})
            keys[mid]={'item_id':mid,'gold_option':str(n%5+1),'private_detail':'NEVER_EXPORT'}
        candidates=[{**deepcopy(old[n]),'item_id':f'R{n}','question':f'New question{n}?',
                     'prompt_text':old[n]['prompt_text'].replace(old[n]['question'],f'New question{n}?'),
                     'prompt_sha256':f'newhash{n}'} for n in range(2)]
        repairs=[{'parent_item_id':f'O{n}','new_item_id':f'R{n}'} for n in range(2)]
        selection={'panels':{'rotations':[{'item_ids':['O0','O2']}],'contrasts':[{'base_id':'O1','contrast_id':'O3'}]}}
        return old,metadata,selection,candidates,repairs,keys

    def test_only_two_replaced_key_inherits_original_options_not_design(self):
        old,md,selection,candidates,repairs,keys=self.bank_fixture();original=deepcopy((old,md,selection,keys))
        bank,newmd,newselection,newkeys,mapping=a.corrected_bank(old,md,selection,candidates,repairs,keys)
        self.assertEqual([r['item_id'] for r in bank],['R0','R1','O2','O3'])
        self.assertEqual(newkeys['R0']['gold_option'],keys['O0']['gold_option'])
        self.assertEqual(newkeys['R1']['gold_option'],keys['O1']['gold_option'])
        self.assertNotIn('O0',newkeys);self.assertNotIn('O1',newkeys)
        self.assertEqual(newmd[2]['base_id'],'R0')
        self.assertEqual(newselection['panels']['rotations'][0]['item_ids'],['R0','O2'])
        self.assertEqual(newselection['panels']['contrasts'][0]['base_id'],'R1')
        self.assertEqual((old,md,selection,keys),original)
        self.assertNotIn('NEVER_EXPORT',json.dumps(bank)+json.dumps(newmd)+json.dumps(newselection))

    def test_unapproved_option_change_rejected(self):
        values=list(self.bank_fixture());values[3][0]['option_1']='Changed choice'
        with self.assertRaises(AssertionError):a.corrected_bank(*values)

    def test_original_key_can_cover_larger_unused_question_pool(self):
        values=list(self.bank_fixture());values[-1]['UNUSED']={'gold_option':'4'}
        *_,keys,mapping=a.corrected_bank(*values)
        self.assertEqual(len(keys),4);self.assertNotIn('UNUSED',keys)

    def test_selection_keeps1134_equivalent_and_drops_all_retired_recoveries(self):
        original=[{'item_id':item,'attempt':attempt,'reported_cost_usd':cost} for item,attempt,cost in
                  [('O0',1,.1),('O0',2,.2),('O1',1,.3),('K',1,.4)]]
        new=[{'item_id':'R0','attempt':1,'reported_cost_usd':.01},{'item_id':'R1','attempt':1,'reported_cost_usd':.02}]
        selected,retired=a.select_replacements(original,new,{'O0','O1'},{'R0','R1'})
        self.assertEqual({r['item_id'] for r in selected},{'K','R0','R1'})
        self.assertEqual(len(retired),3)
        self.assertEqual(a.monetary(selected)['exact_usd'],'0.43')
        self.assertEqual(a.monetary(retired)['exact_usd'],'0.6')

    def test_money_falls_back_reported_preserves_original_accounted_and_unknowns(self):
        aa=[{'reported_cost_usd':.2},{'reported_cost_usd':.3,'accounted_cost_usd':None},
            {'reported_cost_usd':None,'accounted_cost_usd':.4},{'reported_cost_usd':None}]
        self.assertEqual(a.monetary(aa),{'known_usd':.9,'exact_usd':'0.9','reported_attempts':3,'missing_attempts':1})
        self.assertEqual(a.monetary(aa,True)['exact_usd'],'0.5')

    def test_first_and_eventual_never_overwrite_first_failure_with_recovery(self):
        aa=[{'item_id':'R','attempt':1,'status':'http_failure'},{'item_id':'R','attempt':2,'status':'ok'}]
        first,last=a.first_eventual(aa)
        self.assertEqual(first['R']['status'],'http_failure');self.assertEqual(last['R']['status'],'ok')
        with self.assertRaises(AssertionError):a.first_eventual(aa+[dict(aa[0])])

    def test_normalization_native_warnings_not_unusable_choice(self):
        r={'item_id':'R','status':'ok','choice':'3','confidence':.9,'probabilities_valid':False}
        normalized=a.normalize(r,True)
        self.assertEqual(normalized['normalized_choice'],'3')
        self.assertEqual(normalized['normalized_status'],'ok')
        self.assertTrue(normalized['probability_warning'])
        self.assertIsNone(a.normalize(r,False)['normalized_confidence'])

    def test_pooled1136_quantiles_not_average_of_cohort_medians(self):
        benchmark=a.ROOT.parent/'jev-1.14-comparison-benchmark';a.retest.modules(benchmark)
        from analysis_core import metrics,panels,panel_summary
        from text_models import quantiles
        from text_additions import compliance
        records=[];keys={};metadata={}
        for n in range(1136):
            item=f'I{n}';keys[item]={'gold_option':'1'};metadata[item]={'role':'core' if n<640 else 'robustness','level':'1'}
            records.append({'item_id':item,'attempt':1,'status':'ok','choice':'1','reported_cost_usd':.001,
                'http_status':200,'error':'','transport_failure':False,'raw_response':{},'model_returned':'model',
                'provider':'Provider','latency_ms':1 if n<1134 else 1000,'started':{'utc':'2026-10-18T12:00:00Z'},
                'completed':{'utc':'2026-10-18T12:00:01Z'},'usage':{}})
        spec={'label':'Synthetic','model':'model','provider_tag':'provider','provider_name':'Provider',
              'host':'openrouter.ai','path':'/api/v1/chat/completions'}
        selection={'panels':{'rotations':[],'contrasts':[],'candidate_checks':[]}}
        result,normalized,stats=a.summarize('model',spec,records,keys,metadata,selection,(metrics,panels,panel_summary,quantiles,compliance))
        self.assertEqual(result['latency_first_all']['median_ms'],1)
        self.assertNotEqual(result['latency_first_all']['median_ms'],(1+1000)/2)
        self.assertEqual(result['primary']['correct'],1136)
        self.assertEqual(result['by_role']['core']['attempted'],640)
        self.assertEqual(sum(result['dates_toronto'].values()),1136)

    def test_csv_output_contains_only_supplied_fields_and_is_exclusive(self):
        old,*_=self.bank_fixture()
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'questions.csv';a.write_csv(path,old)
            self.assertEqual(a.read_csv(path),old)
            with self.assertRaises(FileExistsError):a.write_csv(path,old)


if __name__=='__main__':unittest.main()

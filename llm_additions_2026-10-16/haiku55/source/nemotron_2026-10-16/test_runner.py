import copy
import unittest

import runner as r


class RunnerTests(unittest.TestCase):
    def good(self):
        return {'http_status':200,'error':'','raw_response':{'model':r.MODEL,'provider':'CoreWeave',
                'choices':[{'message':{'content':'3'},'finish_reason':'stop'}],
                'usage':{'cost':0.00001,'prompt_tokens':200,'completion_tokens':2,
                         'completion_tokens_details':{'reasoning_tokens':0}}}}

    def test_payload_preserves_original_protocol(self):
        q = {'prompt_text':'original full question'}
        p = r.payload(q)
        self.assertEqual(p['messages'],[{'role':'user','content':q['prompt_text']+r.chat.SUFFIX}])
        self.assertEqual(p['max_tokens'],16)
        self.assertNotIn('temperature',p)
        self.assertEqual(p['reasoning'],{'enabled':False})
        self.assertEqual(p['provider']['only'],['coreweave/bf16'])
        self.assertFalse(p['provider']['allow_fallbacks'])

    def test_all_original_items_planned_once(self):
        qs,plan = r.prepare()
        self.assertEqual(len(qs),1136)
        self.assertEqual(len({p['item_id'] for p in plan}),1136)
        self.assertEqual(len({p['wave'] for p in plan}),568)

    def test_strict_id(self):
        response = self.good()
        self.assertEqual(r.parse(response)['status'],'ok')
        for content in ('3 because...',None,'', '6'):
            response['raw_response']['choices'][0]['message']['content'] = content
            self.assertNotEqual(r.parse(response)['status'],'ok')

    def test_truncated_not_usable(self):
        response = self.good()
        response['raw_response']['choices'][0]['finish_reason'] = 'length'
        self.assertNotEqual(r.parse(response)['status'],'ok')

    def test_reasoning_rejected_not_hidden(self):
        for field,value in [('reasoning','explanation'),('reasoning_details',[{'text':'x'}])]:
            response = self.good()
            response['raw_response']['choices'][0]['message'][field] = value
            self.assertEqual(r.parse(response)['status'],'unexpected_reasoning')
        response = self.good()
        response['raw_response']['usage']['completion_tokens_details']['reasoning_tokens'] = 4
        self.assertEqual(r.parse(response)['status'],'unexpected_reasoning')

    def test_provider_and_cost_guard(self):
        response = self.good()
        record = {**response,**r.parse(response)}
        r.check_identity(record)
        for field,value in [('provider','different'),('model_returned','different'),('reported_cost_usd',None)]:
            bad = copy.deepcopy(record)
            bad[field] = value
            with self.assertRaises(AssertionError):
                r.check_identity(bad)


if __name__ == '__main__':
    unittest.main()

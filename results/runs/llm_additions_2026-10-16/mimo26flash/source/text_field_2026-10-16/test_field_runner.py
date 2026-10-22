import unittest
import field_runner as f


class FieldTests(unittest.TestCase):
    def test_distinct_candidate_models_and_pins(self):
        self.assertEqual(len(f.CONFIG),8)
        self.assertEqual(len({v[1] for v in f.CONFIG.values()}),8)
        for model_id, spec in f.CONFIG.items():
            f.configure(model_id)
            p=f.run.payload({'prompt_text':'question'})
            self.assertEqual(p['model'],spec[1])
            self.assertEqual(p['provider']['only'],[spec[2]])
            self.assertFalse(p['provider']['allow_fallbacks'])
            self.assertEqual(p['reasoning'],{'enabled':False})
            self.assertEqual(p['max_tokens'],16)
            self.assertNotIn('temperature',p)

    def test_original_bank_and_message_protocol(self):
        f.configure('haiku55')
        qs,plan=f.run.prepare()
        self.assertEqual(len(qs),1136)
        self.assertEqual(len({p['item_id'] for p in plan}),1136)
        p=f.run.payload(qs[plan[0]['item_id']])
        self.assertEqual(p['messages'][0]['content'],qs[plan[0]['item_id']]['prompt_text']+f.run.chat.SUFFIX)


if __name__=='__main__':
    unittest.main()

import unittest

from answer_ollama import generate, verify_claims, verify_verdict


class LocalAnswerTest(unittest.TestCase):
    def setUp(self):
        self.citation = {"report_id": "100-1", "pdf_page": 33}
        self.chunks = [{"text": "Test before launch and regularly after launch.",
                        "citations": [self.citation]}]

    def test_accepts_real_quote_and_maps_citation(self):
        result = generate("When to test?", self.chunks, ask=lambda _: {
            "answer": "Before and after launch.",
            "evidence": [{"passage": 1, "quote": "before launch and regularly after launch"}],
        })
        self.assertEqual(result["citations"], [self.citation])

    def test_rejects_invented_quote_or_invalid_passage(self):
        for passage, quote in [(1, "test once every week"), (2, "before launch and regularly")]:
            result = generate("When to test?", self.chunks, ask=lambda _: {
                "answer": "Weekly.", "evidence": [{"passage": passage, "quote": quote}],
            })
            self.assertIsNone(result)

    def test_accepts_abstention(self):
        self.assertIsNone(generate("When to test?", self.chunks, ask=lambda _: {
            "answer": "", "evidence": [],
        }))


    def test_claim_check_receives_verified_quotes_and_fails_closed(self):
        draft = {"text": "Before deployment.", "quotes": ["Test before deployment."]}

        def malformed_reply(messages, schema):
            self.assertIn("Test before deployment.", messages[1]["content"])
            self.assertEqual(schema["properties"]["supported"], {"type": "boolean"})
            return {"supported": "true", "reason": "Malformed boolean"}

        self.assertFalse(verify_claims("When to test?", draft, ask=malformed_reply)["supported"])

    def test_field_quote_can_be_verified_with_full_source_row(self):
        chunk = dict(self.chunks[0], kind="row",
                     source_context="MS-3.2-001 | Test before launch. | Confabulation")
        draft = generate("When to test?", [chunk], ask=lambda _: {
            "answer": "Before launch.",
            "evidence": [{"passage": 1, "quote": "Test before launch"}],
        })
        self.assertEqual(draft["table_context"], [chunk["source_context"]])

        def judge(messages, schema):
            payload = messages[1]["content"]
            self.assertIn("MS-3.2-001", payload)
            self.assertIn("Test before launch", payload)
            return {"supported": True, "reason": "The source row identifies the action."}

        self.assertTrue(verify_claims("When to test?", draft, ask=judge,
                                      include_table_context=True)["supported"])

    def test_verdict_only_rejects_explanation_fields(self):
        draft = {"text": "Before deployment.", "quotes": ["Test before deployment."]}
        verdict = verify_verdict("When to test?", draft, ask=lambda *_args, **_kw: {
            "supported": False,
        })
        self.assertIs(verdict, False)
        with self.assertRaisesRegex(ValueError, "Invalid verdict"):
            verify_verdict("When to test?", draft, ask=lambda *_args, **_kw: {
                "supported": True, "reason": "Unexpected field",
            })


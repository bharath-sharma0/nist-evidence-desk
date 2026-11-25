import unittest

from ask_nist import answer_action


class ActionAnswerTest(unittest.TestCase):
    def test_lookup_answers_only_the_requested_supported_field(self):
        class Index:
            def search(self, question, k):
                return [{
                    "text": "GV-1.1-001 | Follow applicable privacy law. | Data Privacy",
                    "citations": [{"report_id": "600-1", "pdf_page": 17}],
                }]

        index = Index()
        labels = {"600-1": {"17": "13"}}
        recommendation = answer_action("What does GV-1.1-001 recommend?", index, labels)
        self.assertEqual(recommendation["text"], "Follow applicable privacy law.")
        risks = answer_action("Which GAI risks does GV-1.1-001 list?", index, labels)
        self.assertEqual(risks["text"], "Data Privacy")
        self.assertIsNone(answer_action("What is the waiver form number for GV-1.1-001?", index, labels))

import unittest

from evaluate_hybrid import fuse


class FusionTest(unittest.TestCase):
    def test_shared_candidate_outranks_candidates_from_one_retriever(self):
        a, b, shared = ({"id": name} for name in ("a", "b", "shared"))
        self.assertEqual(fuse([a, shared], [b, shared], k=2), [shared, a])

    def test_handles_an_empty_ranking_and_caps_results(self):
        a, b = ({"id": name} for name in ("a", "b"))
        self.assertEqual(fuse([], [b, a], k=1), [b])
        self.assertEqual(fuse([], [], k=5), [])

# Provisional BM25 development diagnostic

Scored 32 answerable development items. The 8 abstention items are excluded. Draft gold labels still require manual review.

| Chunking | Evidence Recall@5 | Complete | Fully retrievable in corpus |
| --- | ---: | ---: | ---: |
| A | 54.2% | 15/32 | 32/32 |
| B | 53.1% | 16/32 | 32/32 |
| C | 57.3% | 17/32 | 32/32 |

## Strategy A

| Question type | Evidence Recall@5 | Complete |
| --- | ---: | ---: |
| factual_lookup | 71.8% | 9/13 |
| multi_passage | 50.0% | 2/7 |
| paraphrased | 37.5% | 4/12 |

| Question | Type | Evidence ranks | Excerpts present anywhere |
| --- | --- | --- | ---: |
| nist-001 | factual_lookup | miss | 1/1 |
| nist-002 | factual_lookup | 3 | 1/1 |
| nist-003 | factual_lookup | miss | 1/1 |
| nist-004 | paraphrased | miss | 1/1 |
| nist-005 | paraphrased | miss, 4 | 2/2 |
| nist-006 | multi_passage | 1 | 1/1 |
| nist-007 | multi_passage | miss, miss | 2/2 |
| nist-008 | factual_lookup | miss, miss, 2 | 3/3 |
| nist-009 | multi_passage | miss, miss | 2/2 |
| nist-014 | paraphrased | miss | 1/1 |
| nist-017 | factual_lookup | 1 | 1/1 |
| nist-019 | factual_lookup | 1 | 1/1 |
| nist-020 | paraphrased | 2 | 1/1 |
| nist-021 | factual_lookup | miss | 1/1 |
| nist-022 | paraphrased | 1 | 1/1 |
| nist-024 | paraphrased | 1 | 1/1 |
| nist-027 | factual_lookup | 1 | 1/1 |
| nist-028 | factual_lookup | 2 | 1/1 |
| nist-029 | factual_lookup | 2 | 1/1 |
| nist-030 | factual_lookup | 1 | 1/1 |
| nist-032 | factual_lookup | 2 | 1/1 |
| nist-033 | factual_lookup | 1 | 1/1 |
| nist-037 | paraphrased | miss | 1/1 |
| nist-038 | paraphrased | miss | 1/1 |
| nist-039 | paraphrased | miss | 1/1 |
| nist-040 | paraphrased | 2 | 1/1 |
| nist-041 | paraphrased | miss | 1/1 |
| nist-043 | paraphrased | miss | 1/1 |
| nist-047 | multi_passage | miss, 3 | 2/2 |
| nist-048 | multi_passage | 1, 2 | 2/2 |
| nist-049 | multi_passage | 2, miss | 2/2 |
| nist-050 | multi_passage | miss, 1 | 2/2 |

## Strategy B

| Question type | Evidence Recall@5 | Complete |
| --- | ---: | ---: |
| factual_lookup | 84.6% | 11/13 |
| multi_passage | 35.7% | 2/7 |
| paraphrased | 29.2% | 3/12 |

| Question | Type | Evidence ranks | Excerpts present anywhere |
| --- | --- | --- | ---: |
| nist-001 | factual_lookup | 3 | 1/1 |
| nist-002 | factual_lookup | 2 | 1/1 |
| nist-003 | factual_lookup | 1 | 1/1 |
| nist-004 | paraphrased | miss | 1/1 |
| nist-005 | paraphrased | miss, 3 | 2/2 |
| nist-006 | multi_passage | 1 | 1/1 |
| nist-007 | multi_passage | miss, miss | 2/2 |
| nist-008 | factual_lookup | miss, miss, miss | 3/3 |
| nist-009 | multi_passage | miss, miss | 2/2 |
| nist-014 | paraphrased | miss | 1/1 |
| nist-017 | factual_lookup | 1 | 1/1 |
| nist-019 | factual_lookup | 2 | 1/1 |
| nist-020 | paraphrased | miss | 1/1 |
| nist-021 | factual_lookup | miss | 1/1 |
| nist-022 | paraphrased | 1 | 1/1 |
| nist-024 | paraphrased | 1 | 1/1 |
| nist-027 | factual_lookup | 1 | 1/1 |
| nist-028 | factual_lookup | 1 | 1/1 |
| nist-029 | factual_lookup | 2 | 1/1 |
| nist-030 | factual_lookup | 1 | 1/1 |
| nist-032 | factual_lookup | 4 | 1/1 |
| nist-033 | factual_lookup | 2 | 1/1 |
| nist-037 | paraphrased | miss | 1/1 |
| nist-038 | paraphrased | miss | 1/1 |
| nist-039 | paraphrased | miss | 1/1 |
| nist-040 | paraphrased | 3 | 1/1 |
| nist-041 | paraphrased | miss | 1/1 |
| nist-043 | paraphrased | miss | 1/1 |
| nist-047 | multi_passage | miss, miss | 2/2 |
| nist-048 | multi_passage | 1, 1 | 2/2 |
| nist-049 | multi_passage | miss, miss | 2/2 |
| nist-050 | multi_passage | miss, 2 | 2/2 |

## Strategy C

| Question type | Evidence Recall@5 | Complete |
| --- | ---: | ---: |
| factual_lookup | 87.2% | 11/13 |
| multi_passage | 50.0% | 3/7 |
| paraphrased | 29.2% | 3/12 |

| Question | Type | Evidence ranks | Excerpts present anywhere |
| --- | --- | --- | ---: |
| nist-001 | factual_lookup | 5 | 1/1 |
| nist-002 | factual_lookup | 2 | 1/1 |
| nist-003 | factual_lookup | 1 | 1/1 |
| nist-004 | paraphrased | miss | 1/1 |
| nist-005 | paraphrased | miss, 3 | 2/2 |
| nist-006 | multi_passage | 1 | 1/1 |
| nist-007 | multi_passage | miss, miss | 2/2 |
| nist-008 | factual_lookup | miss, miss, 3 | 3/3 |
| nist-009 | multi_passage | miss, miss | 2/2 |
| nist-014 | paraphrased | miss | 1/1 |
| nist-017 | factual_lookup | 1 | 1/1 |
| nist-019 | factual_lookup | 1 | 1/1 |
| nist-020 | paraphrased | miss | 1/1 |
| nist-021 | factual_lookup | miss | 1/1 |
| nist-022 | paraphrased | 1 | 1/1 |
| nist-024 | paraphrased | 1 | 1/1 |
| nist-027 | factual_lookup | 1 | 1/1 |
| nist-028 | factual_lookup | 1 | 1/1 |
| nist-029 | factual_lookup | 2 | 1/1 |
| nist-030 | factual_lookup | 1 | 1/1 |
| nist-032 | factual_lookup | 4 | 1/1 |
| nist-033 | factual_lookup | 5 | 1/1 |
| nist-037 | paraphrased | miss | 1/1 |
| nist-038 | paraphrased | miss | 1/1 |
| nist-039 | paraphrased | miss | 1/1 |
| nist-040 | paraphrased | 3 | 1/1 |
| nist-041 | paraphrased | miss | 1/1 |
| nist-043 | paraphrased | miss | 1/1 |
| nist-047 | multi_passage | 5, 5 | 2/2 |
| nist-048 | multi_passage | 1, 1 | 2/2 |
| nist-049 | multi_passage | miss, miss | 2/2 |
| nist-050 | multi_passage | miss, 1 | 2/2 |

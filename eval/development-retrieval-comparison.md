# Provisional development retrieval comparison

Reciprocal rank fusion uses up to 30 results per retriever and adds 1/(60 + rank) for each appearance. A missing candidate contributes zero. The same 32 answerable questions and exact excerpt metric are used for every row.

Development labels remain provisional.

BGE model revision 5c38ec7c405ec4b44b94cc5a9bb96e735b38267a. BM25 and BGE rankings are regenerated in this run.

| Chunking | BM25 evidence Recall@5 | BGE evidence Recall@5 | Hybrid evidence Recall@5 | BM25 complete | BGE complete | Hybrid complete |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 54.2% | 34.4% | 48.4% | 15/32 | 10/32 | 14/32 |
| B | 53.1% | 32.8% | 56.2% | 16/32 | 10/32 | 17/32 |
| C | 57.3% | 25.0% | 51.6% | 17/32 | 8/32 | 16/32 |

Complete means all labeled excerpts for a question appear in the top five. Abstention and answer generation are outside this pilot.

## Strategy A

| Question | BM25 ranks | BGE ranks | Hybrid ranks |
| --- | --- | --- | --- |
| nist-001 | miss | miss | 2 |
| nist-002 | 3 | miss | 4 |
| nist-003 | miss | miss | miss |
| nist-004 | miss | miss | miss |
| nist-005 | miss, 4 | miss, miss | miss, 3 |
| nist-006 | 1 | 1 | 1 |
| nist-007 | miss, miss | miss, miss | miss, miss |
| nist-008 | miss, miss, 2 | miss, miss, miss | miss, miss, miss |
| nist-009 | miss, miss | miss, miss | miss, miss |
| nist-014 | miss | 4 | miss |
| nist-017 | 1 | 1 | 1 |
| nist-019 | 1 | miss | 3 |
| nist-020 | 2 | 1 | 1 |
| nist-021 | miss | miss | 1 |
| nist-022 | 1 | 1 | 1 |
| nist-024 | 1 | 1 | 1 |
| nist-027 | 1 | miss | miss |
| nist-028 | 2 | 2 | 1 |
| nist-029 | 2 | miss | miss |
| nist-030 | 1 | miss | miss |
| nist-032 | 2 | miss | 2 |
| nist-033 | 1 | miss | miss |
| nist-037 | miss | miss | miss |
| nist-038 | miss | 3 | 3 |
| nist-039 | miss | miss | miss |
| nist-040 | 2 | 2 | 2 |
| nist-041 | miss | miss | miss |
| nist-043 | miss | miss | miss |
| nist-047 | miss, 3 | 2, miss | miss, miss |
| nist-048 | 1, 2 | 2, 1 | 2, 1 |
| nist-049 | 2, miss | 1, miss | 1, miss |
| nist-050 | miss, 1 | miss, miss | miss, 2 |

## Strategy B

| Question | BM25 ranks | BGE ranks | Hybrid ranks |
| --- | --- | --- | --- |
| nist-001 | 3 | miss | miss |
| nist-002 | 2 | 2 | 1 |
| nist-003 | 1 | miss | miss |
| nist-004 | miss | miss | miss |
| nist-005 | miss, 3 | miss, miss | miss, miss |
| nist-006 | 1 | 1 | 1 |
| nist-007 | miss, miss | miss, miss | miss, miss |
| nist-008 | miss, miss, miss | miss, miss, miss | miss, miss, miss |
| nist-009 | miss, miss | miss, miss | miss, miss |
| nist-014 | miss | miss | miss |
| nist-017 | 1 | 1 | 1 |
| nist-019 | 2 | miss | 1 |
| nist-020 | miss | miss | 3 |
| nist-021 | miss | miss | 2 |
| nist-022 | 1 | 3 | 1 |
| nist-024 | 1 | 1 | 1 |
| nist-027 | 1 | 3 | 1 |
| nist-028 | 1 | miss | 4 |
| nist-029 | 2 | 5 | 3 |
| nist-030 | 1 | 1 | 1 |
| nist-032 | 4 | miss | miss |
| nist-033 | 2 | miss | 5 |
| nist-037 | miss | miss | miss |
| nist-038 | miss | 3 | 1 |
| nist-039 | miss | miss | miss |
| nist-040 | 3 | miss | 4 |
| nist-041 | miss | miss | miss |
| nist-043 | miss | miss | miss |
| nist-047 | miss, miss | miss, miss | 3, 3 |
| nist-048 | 1, 1 | 1, 1 | 1, 1 |
| nist-049 | miss, miss | 2, miss | 1, miss |
| nist-050 | miss, 2 | miss, miss | miss, 3 |

## Strategy C

| Question | BM25 ranks | BGE ranks | Hybrid ranks |
| --- | --- | --- | --- |
| nist-001 | 5 | miss | miss |
| nist-002 | 2 | miss | 2 |
| nist-003 | 1 | miss | 4 |
| nist-004 | miss | miss | miss |
| nist-005 | miss, 3 | miss, miss | miss, miss |
| nist-006 | 1 | 2 | 1 |
| nist-007 | miss, miss | miss, miss | miss, miss |
| nist-008 | miss, miss, 3 | miss, miss, miss | miss, miss, miss |
| nist-009 | miss, miss | miss, miss | miss, miss |
| nist-014 | miss | miss | miss |
| nist-017 | 1 | 1 | 1 |
| nist-019 | 1 | miss | 4 |
| nist-020 | miss | 3 | 2 |
| nist-021 | miss | miss | 4 |
| nist-022 | 1 | 2 | 1 |
| nist-024 | 1 | 1 | 1 |
| nist-027 | 1 | miss | 2 |
| nist-028 | 1 | miss | miss |
| nist-029 | 2 | miss | 1 |
| nist-030 | 1 | 1 | 1 |
| nist-032 | 4 | miss | miss |
| nist-033 | 5 | miss | miss |
| nist-037 | miss | miss | miss |
| nist-038 | miss | 2 | 2 |
| nist-039 | miss | miss | miss |
| nist-040 | 3 | miss | 4 |
| nist-041 | miss | miss | miss |
| nist-043 | miss | miss | miss |
| nist-047 | 5, 5 | miss, miss | 3, 3 |
| nist-048 | 1, 1 | 1, 1 | 1, 1 |
| nist-049 | miss, miss | miss, miss | miss, miss |
| nist-050 | miss, 1 | miss, miss | miss, 1 |

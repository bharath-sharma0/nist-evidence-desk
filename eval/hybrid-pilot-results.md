# Hybrid retrieval pilot

Reciprocal rank fusion uses up to 30 results per retriever and adds 1/(60 + rank) for each appearance. A missing candidate contributes zero. The settings were fixed before the run. The same nine answerable pilot questions and exact excerpt metric are used for every row.

BGE model revision 5c38ec7c405ec4b44b94cc5a9bb96e735b38267a. BM25 and BGE rankings are regenerated in this run.

| Chunking | BM25 evidence Recall@5 | BGE evidence Recall@5 | Hybrid evidence Recall@5 | BM25 complete | BGE complete | Hybrid complete |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 31.5% | 11.1% | 38.9% | 2/9 | 1/9 | 3/9 |
| B | 50.0% | 22.2% | 22.2% | 4/9 | 2/9 | 2/9 |
| C | 53.7% | 11.1% | 33.3% | 4/9 | 1/9 | 3/9 |

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

## Strategy C

| Question | BM25 ranks | BGE ranks | Hybrid ranks |
| --- | --- | --- | --- |
| nist-001 | 5 | miss | miss |
| nist-002 | 3 | miss | 3 |
| nist-003 | 1 | miss | 2 |
| nist-004 | miss | miss | miss |
| nist-005 | miss, 3 | miss, miss | miss, miss |
| nist-006 | 1 | 2 | 1 |
| nist-007 | miss, miss | miss, miss | miss, miss |
| nist-008 | miss, miss, 3 | miss, miss, miss | miss, miss, miss |
| nist-009 | miss, miss | miss, miss | miss, miss |

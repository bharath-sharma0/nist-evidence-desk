# BM25 pilot results

Fixed BM25 settings k1=1.2 and b=0.75. The same nine answerable pilot questions are scored on each chunk dataset. An evidence hit requires the correct report and PDF page plus the entire labeled excerpt in one returned chunk after whitespace normalization. The three abstention cases are excluded.

| Chunking | Macro evidence Recall@5 | At least one excerpt | All excerpts | Available anywhere |
| --- | ---: | ---: | ---: | ---: |
| A | 31.5% | 4/9 | 2/9 | 14/14 |
| B | 50.0% | 5/9 | 4/9 | 14/14 |
| C | 53.7% | 6/9 | 4/9 | 13/14 |

Macro recall averages each question's fraction of excerpts found. Available anywhere is an upper bound imposed by chunk boundaries. These are pilot diagnostics. The final evaluation needs a separate held-out set.

## Strategy A

| Question | First rank per labeled excerpt | Available anywhere |
| --- | --- | ---: |
| nist-001 | miss | 1/1 |
| nist-002 | 3 | 1/1 |
| nist-003 | miss | 1/1 |
| nist-004 | miss | 1/1 |
| nist-005 | miss, 4 | 2/2 |
| nist-006 | 1 | 1/1 |
| nist-007 | miss, miss | 2/2 |
| nist-008 | miss, miss, 2 | 3/3 |
| nist-009 | miss, miss | 2/2 |

## Strategy B

| Question | First rank per labeled excerpt | Available anywhere |
| --- | --- | ---: |
| nist-001 | 3 | 1/1 |
| nist-002 | 2 | 1/1 |
| nist-003 | 1 | 1/1 |
| nist-004 | miss | 1/1 |
| nist-005 | miss, 3 | 2/2 |
| nist-006 | 1 | 1/1 |
| nist-007 | miss, miss | 2/2 |
| nist-008 | miss, miss, miss | 3/3 |
| nist-009 | miss, miss | 2/2 |

## Strategy C

| Question | First rank per labeled excerpt | Available anywhere |
| --- | --- | ---: |
| nist-001 | 5 | 1/1 |
| nist-002 | 3 | 1/1 |
| nist-003 | 1 | 1/1 |
| nist-004 | miss | 1/1 |
| nist-005 | miss, 3 | 2/2 |
| nist-006 | 1 | 1/1 |
| nist-007 | miss, miss | 2/2 |
| nist-008 | miss, miss, 3 | 2/3 |
| nist-009 | miss, miss | 2/2 |

# Development retrieval failure audit

BM25 was rerun at full depth for four recurring misses. A rank is the first positively scored chunk containing the full excerpt on the cited page. Unranked means a matching chunk exists but received no positive keyword score. Unavailable means no chunk contains the full excerpt.

| Question and excerpt | Cited PDF page | A | B | C |
| --- | --- | ---: | ---: | ---: |
| nist-004 excerpt 1 | AI 600-1, p. 10 | 17 | 14 | 20 |
| nist-007 excerpt 1 | AI 600-1, p. 18 | 39 | 40 | 35 |
| nist-007 excerpt 2 | AI 600-1, p. 19 | 189 | 17 | 165 |
| nist-008 excerpt 1 | AI 600-1, p. 51 | 81 | 113 | 164 |
| nist-008 excerpt 2 | AI 600-1, p. 51 | 81 | 37 | 97 |
| nist-008 excerpt 3 | AI 600-1, p. 52 | 2 | 7 | 3 |
| nist-009 excerpt 1 | AI 100-1, p. 29 | 55 | 120 | 92 |
| nist-009 excerpt 2 | AI 100-1, p. 33 | 87 | 49 | 59 |

## Query vocabulary check

The additional query below is a post-hoc diagnostic using the gold term. It is not counted in the benchmark.

- Strategy A, original: 17
- Strategy A, with gold term: 9
- Strategy B, original: 14
- Strategy B, with gold term: 5
- Strategy C, original: 20
- Strategy C, with gold term: 6

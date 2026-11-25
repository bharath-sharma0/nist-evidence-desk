# BGE-small dense retrieval pilot

BAAI/bge-small-en-v1.5 revision 5c38ec7c405ec4b44b94cc5a9bb96e735b38267a. CPU ONNX inference, normalized CLS embeddings, cosine similarity and the model's retrieval query prefix.

The same nine answerable questions and excerpt-matching metric are used for BM25 and dense retrieval. These pilot results do not estimate held-out performance.

| Chunking | BM25 evidence Recall@5 | Dense evidence Recall@5 | BM25 complete | Dense complete | Chunks over 512 tokens | Max tokens | CPU encoding time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 31.5% | 11.1% | 2/9 | 1/9 | 6/488 | 821 | 51.0 s |
| B | 50.0% | 22.2% | 4/9 | 2/9 | 7/264 | 615 | 19.0 s |
| C | 53.7% | 11.1% | 4/9 | 1/9 | 0/403 | 368 | 19.5 s |

The longest prefixed question was 43 tokens.
Encoding time includes tokenization and excludes model loading.

## Strategy A

| Question | BM25 excerpt ranks | Dense excerpt ranks |
| --- | --- | --- |
| nist-001 | miss | miss |
| nist-002 | 3 | miss |
| nist-003 | miss | miss |
| nist-004 | miss | miss |
| nist-005 | miss, 4 | miss, miss |
| nist-006 | 1 | 1 |
| nist-007 | miss, miss | miss, miss |
| nist-008 | miss, miss, 2 | miss, miss, miss |
| nist-009 | miss, miss | miss, miss |

## Strategy B

| Question | BM25 excerpt ranks | Dense excerpt ranks |
| --- | --- | --- |
| nist-001 | 3 | miss |
| nist-002 | 2 | 2 |
| nist-003 | 1 | miss |
| nist-004 | miss | miss |
| nist-005 | miss, 3 | miss, miss |
| nist-006 | 1 | 1 |
| nist-007 | miss, miss | miss, miss |
| nist-008 | miss, miss, miss | miss, miss, miss |
| nist-009 | miss, miss | miss, miss |

## Strategy C

| Question | BM25 excerpt ranks | Dense excerpt ranks |
| --- | --- | --- |
| nist-001 | 5 | miss |
| nist-002 | 3 | miss |
| nist-003 | 1 | miss |
| nist-004 | miss | miss |
| nist-005 | miss, 3 | miss, miss |
| nist-006 | 1 | 2 |
| nist-007 | miss, miss | miss, miss |
| nist-008 | miss, miss, 3 | miss, miss, miss |
| nist-009 | miss, miss | miss, miss |

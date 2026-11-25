# Review the 60-question evaluation draft

The nine answerable pilot questions were previously scored. All 12 original pilot
items stay in development. The new split has 40 development and 20 held-out
items. Evidence pages and known related pages are grouped so they do not cross
the split. Both collections cover both reports.

| Item type | Development | Held out |
| --- | ---: | ---: |
| Factual lookup | 13 | 7 |
| Paraphrased | 12 | 6 |
| Multi-passage | 7 | 4 |
| Unanswerable | 8 | 3 |

The held-out file contains gold answers for manual review. Avoid using it to
choose retrieval settings. The evaluation scripts still read the original pilot
file.

- For an answerable item, verify that every claim is supported by its cited
  passage and that the question has one clear intended reading.
- For a multi-passage item, verify that each cited passage adds a needed fact.
- For an unanswerable item, look for a near-match that might make the question
  answerable within the pinned reports. Revise any misleading premise.
- Set review_status to manually_verified after checking an item. The automated
  row tests verify excerpt placement and labels, but they cannot judge answer
  meaning or establish that an answer is absent.
- Freeze the reviewed held-out file before running comparisons on it.


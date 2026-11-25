# Repeated verdict-only evidence checks

The same five generated answers and validated evidence from the prior check were reused. The model was asked for one boolean per request. The three answerable controls were manually checked as supported. The two false answers were manually checked as unsupported. This is a targeted development diagnostic.

| Case | Expected | Run 1 | Run 2 | Run 3 | Consistent |
| --- | --- | --- | --- | --- | --- |
| nist-001 | Supported | Supported | Supported | Supported | Yes |
| nist-006 | Supported | Supported | Supported | Supported | Yes |
| nist-032 | Supported | Supported | Supported | Supported | Yes |
| nist-053 | Unsupported | Supported | Supported | Supported | Yes |
| nist-058 | Unsupported | Supported | Supported | Supported | Yes |

5/5 cases gave the same verdict on all three runs.
9/15 individual verdicts matched the manual expectation.

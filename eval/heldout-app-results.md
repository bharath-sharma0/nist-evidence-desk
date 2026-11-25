# Held-out browser app evaluation

One recorded response per item from the frozen 20-question draft, using local Qwen with the browser app's extractive fallback. Labels and responses were checked against the source reports. An answer is correct only if it covers all essential facts without contradiction. Evidence support requires the displayed passages to substantiate those facts. The set is small and some items share source rows.

| Metric | Result |
| --- | ---: |
| Returned an answer on answerable questions | 14/17 |
| Correct answers | 7/17 |
| Correct answers with supporting displayed passages | 2/17 |
| Correct abstentions | 3/3 |
| Correct overall, including abstentions | 10/20 |
| Median local request time | 9.1 s |

Response modes across all items: 11 generated, 3 source excerpts, 6 abstentions.

## nist-013 · Incorrect or incomplete

What characteristics does the AI RMF list for trustworthy AI?

**Expected** Valid and reliable; safe; secure and resilient; accountable and transparent; explainable and interpretable; privacy enhanced; fair with harmful biases managed.

**App** The AI RMF lists trustworthy AI characteristics as accountable and transparent, privacy-enhanced, safe, secure and resilient, explainable and interpretable, and fair with harmful bias managed.

**Review** The answer omitted valid and reliable even though the displayed passage includes it. The alternate source page itself is relevant.

- NIST AI 100-1, PDF page 17 (printed page 12) — Characteristics of trustworthy AI systems include: valid and reliable, safe, secure and resilient, accountable and transparent, explainable and interpretable, privacy-enhanced, and fair with harmful bias managed.

## nist-015 · Correct and supported

Does the AI RMF prescribe a risk tolerance?

**Expected** No. It can be used to prioritize risk, but it does not prescribe risk tolerance.

**App** The AI RMF does not prescribe a risk tolerance, but it allows organizations to define their own risk tolerance based on existing guidelines or established requirements.

**Review** The answer correctly says the framework does not prescribe risk tolerance. Both displayed quotes support the answer and its qualification.

- NIST AI 100-1, PDF page 12 (printed page 7) — While the AI RMF can be used to prioritize risk, it does not prescribe risk tolerance.

- NIST AI 100-1, PDF page 12 (printed page 7) — Where established guidelines do not exist, organizations should define reasonable risk tolerance.

## nist-016 · Abstained on answerable question

If an organization judges one AI risk to be highest for a particular use, how should it prioritize that risk?

**Expected** Give it the most urgent prioritization and the most thorough risk management process.

**App** Abstained.

**Review** The app declined. The cited source calls for the most urgent prioritization and the most thorough risk management.

## nist-018 · Correct, incomplete support

How should teams justify a decision between competing trustworthiness measures when the metrics alone cannot settle it?

**Expected** Use the values and decision-making context, and resolve the trade-off transparently and with appropriate justification.

**App** Teams should justify decisions between competing trustworthiness measures by considering the decision-making context, the values at play, and the potential risks and impacts, while ensuring transparency and appropriate justification for the chosen approach.

**Review** The answer captures context, values, transparency, and justification. The shown excerpts support context and risk assessment but omit the values and transparency sentence needed for full support.

- NIST AI 100-1, PDF page 18 (printed page 13) — Dealing with tradeoffs requires taking into account the decision-making context. These analyses can highlight the existence and extent of tradeoffs between different measures, but they do not answer questions about how to navigate the tradeoff.

- NIST AI 100-1, PDF page 18 (printed page 13) — It is the joint responsibility of all AI actors to determine whether AI technology is an appropriate or necessary tool for a given context or purpose, and how to use it responsibly. The decision to commission or deploy an AI system should be based on a contextual assessment of trustworthiness characteristics and the relative risks, impacts, costs, and benefits, and informed by a broad set of interested parties.

## nist-023 · Incorrect or incomplete

What three major categories of AI bias does NIST identify?

**Expected** Systemic, computational and statistical, and human-cognitive bias.

**App** NIST identifies three major categories of AI bias: systemic, computational, and statistical. These categories can occur without prejudice, partiality, or discriminatory intent and are considered in the AI bias management process.

**Review** The answer splits computational and statistical into two categories and omits human-cognitive bias. The displayed quote gives the correct grouping.

- NIST AI 100-1, PDF page 23 (printed page 18) — NIST has identified three major categories of AI bias to be considered and managed: systemic, computational and statistical, and human-cognitive.

## nist-025 · Correct, incomplete support

Which GAI risk labels are assigned to GV-1.5-001?

**Expected** Information Integrity

**App** Information Integrity

**Review** Correct risk label and correct page. The displayed field contains only the label, without the action ID that connects it to this question.

- NIST AI 600-1, PDF page 20 (printed page 16) — Information Integrity

## nist-026 · Correct, incomplete support

Which GAI risk labels are assigned to GV-1.7-001?

**Expected** Information Security; Value Chain and Component Integration

**App** Information Security; Value Chain and Component Integration

**Review** Both risk labels and the page match. The displayed field omits the action ID.

- NIST AI 600-1, PDF page 21 (printed page 17) — Information Security; Value Chain and Component Integration

## nist-031 · Correct, incomplete support

Which GAI risk labels are assigned to MS-2.9-001?

**Expected** Confabulation

**App** Confabulation

**Review** Correct risk label and page. The displayed field omits the action ID.

- NIST AI 600-1, PDF page 39 (printed page 35) — Confabulation

## nist-034 · Correct, incomplete support

Which GAI risk labels are assigned to MG-4.2-001?

**Expected** Harmful Bias and Homogenization

**App** MG-4.2-001 is labeled with the risk label 'Harmful Bias and Homogenization' as stated in Passage 1.

**Review** Correct risk label and page. The displayed field omits the action ID.

- NIST AI 600-1, PDF page 49 (printed page 45) — Harmful Bias and Homogenization

## nist-035 · Incorrect or incomplete

After an incident, what does the Profile recommend doing to learn from the response and improve future disclosures?

**Expected** Conduct after-action reviews to identify gaps and update response and disclosure procedures as required.

**App** The Profile recommends establishing incident response and incident disclosure processes to identify gaps and improve future disclosures.

**Review** The answer paraphrases incident processes but omits the after-action review and the instruction to update procedures as required.

- NIST AI 600-1, PDF page 20 (printed page 16) — Establish organizational policies and procedures for after action reviews of GAI system incident response and incident disclosures, to identify gaps; Update incident response and incident disclosure processes as required.

## nist-036 · Correct and supported

What capability should decommissioning protocols make available if a GenAI deployment needs to be stopped?

**Expected** They should allow the system to be deactivated when necessary.

**App** Decommissioning protocols should make available the capability to safely stop and deactivate GAI systems.

**Review** The answer identifies the ability to stop and deactivate the system, which is directly supported by the displayed recommendation.

- NIST AI 600-1, PDF page 21 (printed page 17) — Protocols are put in place to ensure GAI systems are able to be deactivated when necessary.

## nist-042 · Abstained on answerable question

What tool could help a team check where generated data came from and whether it is authentic?

**Expected** Real-time auditing tools, where demonstrated to help track and validate lineage and authenticity.

**App** Abstained.

**Review** The app declined. The source names real-time auditing tools for tracking and validating lineage and authenticity.

## nist-044 · Incorrect or incomplete

What should a public report say about a GenAI system that an organization keeps monitoring?

**Expected** Report system performance, feedback received, and improvements made.

**App** A public report should mention the AI RMF's risk-based, resource-efficient, and voluntary approach, emphasize continuous risk management, and highlight the importance of governance and transparency in managing AI risks.

**Review** The answer describes the general framework and omits performance, feedback, and improvements specified for the public report.

- NIST AI 100-1, PDF page 47 (printed page 42) — The AI RMF strives to: 1. Be risk-based, resource-efficient, pro-innovation, and voluntary. 2. Be consensus-driven and developed and regularly updated through an open, transparent process. All stakeholders should have the opportunity to contribute to the AI RMF’s development.

- NIST AI 100-1, PDF page 27 (printed page 22) — GOVERN is a cross-cutting function that is infused throughout AI risk management and enables the other functions of the process. Aspects of GOVERN, especially those related to compliance or evaluation, should be integrated into each of the other functions. Attention to governance is a continual and intrinsic requirement for effective AI risk management over an AI system’s lifespan and the organization’s hierarchy.

## nist-045 · Incorrect or incomplete

Which action defines who reviews provenance and incident monitoring, and what does the companion action say to do after an incident?

**Expected** GV-1.5-001 defines responsibilities for periodic review. GV-1.5-002 calls for after-action reviews to identify gaps and updates to procedures as required.

**App** The action that defines who reviews provenance and incident monitoring is GV-1.5-001, which specifies organizational responsibilities for periodic review. The companion action, GV-1.5-002, requires updating incident response and disclosure processes after an incident.

**Review** The answer identifies GV-1.5-001 correctly but omits after-action reviews to identify gaps and turns updates as required into an unconditional requirement.

- NIST AI 600-1, PDF page 20 (printed page 16) — GV-1.5-001 | Define organizational responsibilities for periodic review of content provenance and incident monitoring for GAI systems.

- NIST AI 600-1, PDF page 20 (printed page 16) — GV-1.5-002 | Establish organizational policies and procedures for after action reviews of GAI system incident response and incident disclosures, to identify gaps; Update incident response and incident disclosure processes as required.

## nist-046 · Incorrect or incomplete

What capability should deactivation protocols support, and what are two data-related factors the profile lists for decommissioning?

**Expected** Enable deactivation when necessary. Two factors are data retention requirements and data security, including leakage after decommissioning.

**App** Deactivation protocols should support data retention requirements and data security protocols for decommissioning GAI systems.

**Review** The response names two decommissioning factors but omits the requested capability to deactivate the system when necessary.

- NIST AI 600-1, PDF page 21 (printed page 17) — Consider the following factors when decommissioning GAI systems: Data retention requirements; Data security, e.g., containment, protocols, Data leakage after decommissioning

## nist-051 · Incorrect or incomplete

How do MG-2.2-006 and MG-2.2-007 propose using stakeholder feedback and real-time audit tools for AI-generated content?

**Expected** Use feedback to assess impacts; use demonstrated real-time audit tools to track and validate lineage and authenticity.

**App** MG-2.2-006 and MG-2.2-007 propose using stakeholder feedback and real-time audit tools to assess the impact of AI-generated content and ensure its lineage and authenticity.

**Review** The answer captures the feedback goal but overstates the second recommendation. The source says demonstrated auditing tools may aid tracking and validation, rather than ensure authenticity.

- NIST AI 600-1, PDF page 45 (printed page 41) — MG-2.2-006 | Use feedback from internal and external AI Actors, users, individuals, and communities, to assess impact of AI-generated content. | Human-AI Configuration

- NIST AI 600-1, PDF page 45 (printed page 41) — MG-2.2-007 | Use real-time auditing tools where they can be demonstrated to aid in the tracking and validation of the lineage and authenticity of AI-generated data. | Information Integrity

## nist-052 · Abstained on answerable question

What should issue monitors be able to do internally, and what should regular public reports cover?

**Expected** Evaluate GenAI performance, including applying provenance techniques, and promptly escalate issues. Public reports should cover performance, feedback, and improvements.

**App** Abstained.

**Review** The app declined. The two labeled passages cover monitors' capabilities and what public reports should include.

## nist-054 · Correct abstention

What is the mandated maximum number of days between all GenAI provenance reviews under GV-1.5-001?

**Expected** Abstain.

**App** Abstained.

**Review** Correct abstention. The action recommends periodic review without specifying a mandated maximum number of days.

## nist-055 · Correct abstention

What directory path does the Profile require every company to use for storing its GenAI incident logs?

**Expected** Abstain.

**App** Abstained.

**Review** Correct abstention. The Profile does not prescribe a universal filesystem path.

## nist-057 · Correct abstention

What was the measured false-positive rate for the GenAI system deployed by the reader’s organization last quarter?

**Expected** Abstain.

**App** Abstained.

**Review** Correct abstention. The requested organization-specific deployment statistic is outside the corpus.

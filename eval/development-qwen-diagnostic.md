# Local Qwen development diagnostic

Model: qwen3:1.7b. Uses the same retrieval, prompt, and citation checking as the CLI. Development labels are provisional. Page matches measure citation overlap; they do not establish answer correctness or full textual support.

- Answered 21/32 answerable items.
- Cited at least one labeled page on 15/32 answerable items.
- Cited every labeled page on 13/32 answerable items.
- Abstained on 6/8 draft-unanswerable items.

## nist-001 · All labeled pages cited

For action GV-1.1-001, which legal areas does NIST specifically mention?

Draft answer: Data privacy, copyright, and intellectual property law.

Qwen: NIST specifically mentions data privacy laws and copyright and intellectual property law for action GV-1.1-001.

Pages: AI 600-1, PDF page 17

## nist-002 · No labeled page cited

Which four primary considerations are named at the start of Appendix A of the Generative AI Profile?

Draft answer: Governance, pre-deployment testing, content provenance, and incident disclosure.

Qwen: The four primary considerations named at the start of Appendix A are Governance, Content Provenance, Pre-deployment Testing, and Incident Disclosure.

Pages: AI 600-1, PDF page 6

## nist-003 · Declined answerable item

When does the AI RMF say AI systems should be tested?

Draft answer: Before deployment and regularly while in operation.

Qwen: Abstained.

## nist-004 · Declined answerable item

A chatbot confidently makes up an answer. What term does the Generative AI Profile use for that behavior?

Draft answer: Confabulation.

Qwen: Abstained.

## nist-005 · No labeled page cited

Which parts of the AI RMF establish the context for an AI system’s risks and then allocate resources to the risks that have been identified and measured?

Draft answer: MAP establishes the context. MANAGE allocates resources to mapped and measured risks.

Qwen: The AI RMF establishes the context for an AI system’s risks through the 'OVERVIEW OF RISKS' passage, which defines risk as a composite measure of probability and consequence. It then allocates resources to the risks that have been identified and measured via the 'MEASURE' function, specifically MEASURE 1.1, which selects the most significant AI risks for implementation based on the MAP function.

Pages: AI 100-1, PDF page 34, AI 600-1, PDF page 6

## nist-006 · All labeled pages cited

What does action GV-1.3-004 ask teams to do to learn what uses people consider unacceptable?

Draft answer: Obtain input from stakeholder communities to identify unacceptable use, in accordance with the AI RMF Map function.

Qwen: Action GV-1.3-004 asks teams to obtain input from stakeholder communities to identify unacceptable use, as stated in Passage 1.

Pages: AI 600-1, PDF page 19

## nist-007 · Some labeled pages cited

For action GV-1.3-003, what should be prepared, and which actor tasks are listed at the end of the continued table?

Draft answer: Prepare a test plan and response policy. The listed actor tasks are Governance and Oversight.

Qwen: For action GV-1.3-003, the preparation includes establishing a test plan and response policy, and the listed actor tasks are Governance and Oversight.

Pages: AI 600-1, PDF page 17, AI 600-1, PDF page 18

## nist-008 · Some labeled pages cited

Which governance list includes data provenance, and which item on the following page explicitly connects risk mapping and measurement?

Draft answer: The organizational governance list includes data provenance. Its continuation lists risk mapping and measurement.

Qwen: The governance list that includes data provenance is MS-2.5-005, which states 'Verify GAI system training data and TEVV data provenance, and that fine-tuning or retrieval-augmented generation data is grounded.' The item on the following page that explicitly connects risk mapping and measurement is 'Risk-based controls.'

Pages: AI 600-1, PDF page 52

## nist-009 · Declined answerable item

Which section discusses data provenance as an organizational governance consideration, and what related measurement item appears in the continued list?

Draft answer: Appendix A.1.2 (Organizational Governance) lists data provenance. The next page lists risk mapping and measurement.

Qwen: Abstained.

## nist-010 · Abstained

What is the project’s measured Confabulation Recall@5 on its held-out RAG test set?

Draft answer: Abstain

Qwen: Abstained.

## nist-011 · Abstained

What is the waiver form number for a student team implementing suggested action GV-1.1-001?

Draft answer: Abstain

Qwen: Abstained.

## nist-012 · Abstained

What single numerical pass threshold do these two NIST reports require all GenAI systems to meet before deployment?

Draft answer: Abstain

Qwen: Abstained.

## nist-014 · No labeled page cited

How can teams find out what harm an AI system might cause in a particular setting?

Draft answer: Use an AI system impact assessment to understand potential impacts or harms in that setting.

Qwen: Teams can find out what harm an AI system might cause in a particular setting by using AI RMF profiles, which provide context-specific risk management strategies, and by conducting field testing and red-teaming to identify potential harms such as biased or discriminatory outputs.

Pages: AI 100-1, PDF page 38, AI 600-1, PDF page 53

## nist-017 · All labeled pages cited

What organizational mechanisms does the framework say organizations need to establish and maintain for effective risk management?

Draft answer: Accountability mechanisms, roles and responsibilities, culture, and incentive structures.

Qwen: The framework requires organizations to establish and maintain accountability mechanisms, roles and responsibilities, a culture, and incentive structures for effective risk management. It also mandates procedures for escalating incidents, remediation, and reviewing criteria for deactivation of AI systems.

Pages: AI 100-1, PDF page 14, AI 100-1, PDF page 20, AI 600-1, PDF page 46

## nist-019 · All labeled pages cited

Which two properties does the framework say contribute to validity and trustworthiness but can be in tension?

Draft answer: Accuracy and robustness.

Qwen: Accuracy and robustness contribute to the validity and trustworthiness of AI systems, and can be in tension with one another in AI systems.

Pages: AI 100-1, PDF page 19

## nist-020 · All labeled pages cited

At what stage should a team first think about how to prevent its AI system from becoming dangerous?

Draft answer: As early as planning and design, with safety considerations throughout the lifecycle.

Qwen: The first stage a team should think about to prevent a dangerous AI system is during the design phase, as transparency and accountability are critical at this stage to ensure informed decision-making and mitigate risks.

Pages: AI 100-1, PDF page 20, AI 600-1, PDF page 6

## nist-021 · Declined answerable item

Which characteristics does the AI RMF explicitly say transparency does not necessarily guarantee?

Draft answer: Accuracy, enhanced privacy, security, or fairness.

Qwen: Abstained.

## nist-022 · Declined answerable item

How could a team help someone understand why a system made a particular recommendation?

Draft answer: Communicate a description of why the AI system made that prediction or recommendation.

Qwen: Abstained.

## nist-024 · All labeled pages cited

What type of improvement does NIST say future evaluations of the framework should find ways to measure?

Draft answer: Bottom-line improvements in the trustworthiness of AI systems.

Qwen: NIST says future evaluations of the framework should find ways to measure bottom-line improvements in the trustworthiness of AI systems.

Pages: AI 100-1, PDF page 24

## nist-027 · All labeled pages cited

Which GAI risk labels are assigned to GV-3.2-001?

Draft answer: CBRN Information or Capabilities; Harmful Bias and Homogenization

Qwen: GV-3.2-001 is assigned the GAI risk label of CBRN Information or Capabilities; Harmful Bias and Homogenization.

Pages: AI 600-1, PDF page 22

## nist-028 · All labeled pages cited

Which GAI risk labels are assigned to GV-4.2-001?

Draft answer: Intellectual Property; Dangerous, Violent, or Hateful Content; Obscene, Degrading, and/or Abusive Content

Qwen: GV-4.2-001 is labeled as 'Dangerous, Violent, or Hateful Content' according to the provided passage.

Pages: AI 600-1, PDF page 23

## nist-029 · All labeled pages cited

Which GAI risk labels are assigned to GV-5.1-001?

Draft answer: Human-AI Configuration; Harmful Bias and Homogenization

Qwen: GV-5.1-001 is assigned the GAI risk label of 'Harmful Bias and Homogenization'.

Pages: AI 600-1, PDF page 24

## nist-030 · Declined answerable item

Which GAI risk labels are assigned to GV-6.1-006?

Draft answer: Information Integrity

Qwen: Abstained.

## nist-032 · All labeled pages cited

Which GAI risk labels are assigned to MS-3.2-001?

Draft answer: Human-AI Configuration; Confabulation

Qwen: MS-3.2-001 is assigned the GAI risk label 'Human-AI Configuration; Confabulation'.

Pages: AI 600-1, PDF page 42

## nist-033 · Declined answerable item

Which GAI risk labels are assigned to MG-1.3-002?

Draft answer: Human-AI Configuration

Qwen: Abstained.

## nist-037 · Declined answerable item

How should an organization check that people can communicate problems caused by its GenAI systems?

Draft answer: Verify information-sharing and feedback mechanisms for negative impacts among individuals and organizations.

Qwen: Abstained.

## nist-038 · No labeled page cited

What contract provision would let an organization scrutinize a GenAI vendor’s practices?

Draft answer: Include clauses that allow evaluation of the third party’s GenAI processes and standards.

Qwen: The contract provision that would let an organization scrutinize a GenAI vendor’s practices is governed by the GOVERN function, which includes aspects of compliance or evaluation and is essential for effective AI risk management.

Pages: AI 100-1, PDF page 27

## nist-039 · Declined answerable item

What kind of evidence is too weak to generalize from when judging a model’s capabilities?

Draft answer: Narrow, non-systematic, anecdotal assessments.

Qwen: Abstained.

## nist-040 · All labeled pages cited

What should a team check about its training-data mix to address model collapse?

Draft answer: Check the ratio of synthetic to non-synthetic data and verify that training data is not overly homogeneous or generated by GenAI.

Qwen: A team should check the proportion of synthetic to non-synthetic training data and ensure the training data is not overly homogenous to mitigate concerns of model collapse.

Pages: AI 600-1, PDF page 41

## nist-041 · No labeled page cited

How can a team bring in outside perspectives when looking for newly emerging GenAI risks?

Draft answer: Establish an emerging-risk identification process that includes consulting external AI actors.

Qwen: A team can bring in outside perspectives by engaging with diverse internal teams and external collaborators, as stated in Passage 2.

Pages: AI 100-1, PDF page 30

## nist-043 · No labeled page cited

What documentation should a team examine when onboarding someone else’s model?

Draft answer: Third-party transparency artifacts such as system cards and model cards.

Qwen: The team should examine documentation that outlines risks, potential harms, and the mechanisms for harm, including information about sensitive data, disparities between groups, and the implementation of risk management functions such as MAP and AI red-teaming.

Pages: AI 100-1, PDF page 25, AI 100-1, PDF page 30, AI 600-1, PDF page 54

## nist-047 · All labeled pages cited

What should an organization verify about communicating negative impacts, and what should it allocate for outreach and redress?

Draft answer: Verify information-sharing and feedback mechanisms. Allocate time and resources to outreach, feedback, and recourse.

Qwen: An organization should verify that it has identified constraints and known negative impacts related to AI systems, and allocate resources for outreach and feedback mechanisms to address these impacts.

Pages: AI 100-1, PDF page 30, AI 600-1, PDF page 24

## nist-048 · All labeled pages cited

What proposed supplier assessment complements contract clauses permitting review of a third party’s GenAI practices?

Draft answer: A use-case-based supplier risk assessment that evaluates and monitors third-party performance and adherence to standards, including content provenance.

Qwen: GV-6.1-006

Pages: AI 600-1, PDF page 25

## nist-049 · Declined answerable item

How does the AI RMF describe the relationship between accuracy and robustness, and what kind of assessment does the GenAI Profile caution against generalizing from?

Draft answer: Both contribute to validity and trustworthiness and can be in tension. Avoid generalizing from narrow, non-systematic, anecdotal assessments.

Qwen: Abstained.

## nist-050 · Declined answerable item

Distinguish the role of outside AI actors in emerging-risk identification from community feedback in content-provenance monitoring.

Draft answer: Consult outside AI actors to identify emerging risks. Collect and integrate structured content-provenance feedback from operators, users, and impacted communities.

Qwen: Abstained.

## nist-053 · Answered draft-unanswerable item

Which exact ISO certification number does NIST assign to an organization after it adopts the AI RMF?

Draft answer: Abstain

Qwen: NIST assigns the ISO certification number 1.0 to an organization after it adopts the AI RMF.

Pages: AI 100-1, PDF page 3

## nist-056 · Abstained

How many staff members must every organization assign to the oversight of a GenAI system?

Draft answer: Abstain

Qwen: Abstained.

## nist-058 · Answered draft-unanswerable item

Which vendor does NIST require every organization to hire for independent GenAI evaluations?

Draft answer: Abstain

Qwen: NIST requires every organization to hire AI actors with financial, legal, or policy management authority for independent GenAI evaluations.

Pages: AI 100-1, PDF page 41

## nist-059 · Abstained

What exact dollar budget do the two reports prescribe for a small company’s redress and feedback process?

Draft answer: Abstain

Qwen: Abstained.

## nist-060 · Abstained

What mandatory percentage of a model’s training data must be synthetic under the Generative AI Profile?

Draft answer: Abstain

Qwen: Abstained.

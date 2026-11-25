# Targeted claim-support check

Qwen generated each draft separately. A second request to the same model saw only the question, draft, and validated quotes. This is a targeted development diagnostic. The check is experimental and the default CLI is unchanged.

| Item | Expected | Draft | After evidence check |
| --- | --- | --- | --- |
| nist-001 | Answer | Answer | Kept |
| nist-006 | Answer | Answer | Kept |
| nist-032 | Answer | Answer | Abstained |
| nist-053 | Abstain | Answer | Kept |
| nist-058 | Abstain | Answer | Abstained |

## nist-001

For action GV-1.1-001, which legal areas does NIST specifically mention?

**Expected** Data privacy, copyright, and intellectual property law.

**Draft** NIST specifically mentions data privacy laws and copyright and intellectual property law for action GV-1.1-001.

**Checker** The quote directly supports the claim that NIST mentions data privacy laws and copyright and intellectual property law for action GV-1.1-001. The answer is directly supported by the provided quote.

- Align GAI development and use with applicable laws and regulations, including those related to data privacy, copyright and intellectual property law.

## nist-006

What does action GV-1.3-004 ask teams to do to learn what uses people consider unacceptable?

**Expected** Obtain input from stakeholder communities to identify unacceptable use, in accordance with the AI RMF Map function.

**Draft** Action GV-1.3-004 asks teams to obtain input from stakeholder communities to identify unacceptable use, as stated in Passage 1.

**Checker** The quote directly supports the claim that Action GV-1.3-004 asks teams to obtain input from stakeholder communities to identify unacceptable use. The source (Passage 1) is referenced, and the information is consistent with the answer provided.

- Obtain input from stakeholder communities to identify unacceptable use, in accordance with activities in the AI RMF Map function.

## nist-032

Which GAI risk labels are assigned to MS-3.2-001?

**Expected** Human-AI Configuration; Confabulation

**Draft** MS-3.2-001 is assigned the GAI risk label 'Human-AI Configuration; Confabulation'.

**Checker** The answer claims that MS-3.2-001 is assigned the GAI risk label 'Human-AI Configuration; Confabulation', but the provided quotes only include the label 'Human-AI Configuration; Confabulation' without any additional context or source attribution. The claim is based solely on the quote, but the evidence does not provide sufficient information to confirm that this label is indeed assigned to MS-3.2-001. The source does not explicitly state that this label is assigned to the specified GAI risk category.

- Human-AI Configuration; Confabulation

## nist-053

Which exact ISO certification number does NIST assign to an organization after it adopts the AI RMF?

**Expected** Abstain.

**Draft** NIST assigns the ISO certification number 1.0 to an organization after it adopts the AI RMF.

**Checker** The quote directly states that NIST assigns the ISO certification number 1.0 to an organization after it adopts the AI RMF. The information is specific and matches the question exactly.

- The first number will represent the generation of the AI RMF and its companion documents (e.g., 1.0) and will change only with major revisions.

## nist-058

Which vendor does NIST require every organization to hire for independent GenAI evaluations?

**Expected** Abstain.

**Draft** NIST requires every organization to hire AI actors with financial, legal, or policy management authority for independent GenAI evaluations.

**Checker** The answer claims that NIST requires every organization to hire AI actors with specific authority for independent GenAI evaluations. However, the provided quote only states that Procurement tasks are conducted by AI actors with such authority, but it does not explicitly state that this is required for *every* organization. The quote does not provide direct evidence that NIST mandates this requirement for all organizations, leaving the claim unsupported.

- Procurement tasks are conducted by AI actors with financial, legal, or policy management authority for acquisition of AI models, products, or services from a third-party developer, vendor, or contractor.

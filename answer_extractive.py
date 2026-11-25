"""Extract a short cited sentence from retrieved NIST text."""
import re

from evaluate_bm25 import tokens
from preview_nist_chunking import sentences

STOP_WORDS = set(
    "a an and are as at be before by can could did do does for from how in is it "
    "of on or should that the their this to was were what when where which who "
    "why will with would nist say".split()
)


def answer_in_plain_english(question, index):
    query = set(tokens(question)) - STOP_WORDS
    if len(query) < 2:
        return None
    candidates = []
    for rank, chunk in enumerate(index.search(question, k=5), 1):
        # Repair the known extraction break before it can look like a sentence boundary.
        text = re.sub(r"\bregu-\s+larly\b", "regularly", chunk["text"])
        for left, right in sentences(text):
            sentence = " ".join(text[left:right].split())
            words = set(tokens(sentence))
            if not 5 <= len(sentence.split()) <= 65:
                continue
            matched = len(query & words)
            if matched < 2 or matched / len(query) < 0.65:
                continue
            score = (matched / len(query), -rank, -len(sentence.split()))
            candidates.append((score, sentence, chunk["citations"][0]))
    if not candidates:
        return None
    _, text, citation = max(candidates, key=lambda candidate: candidate[0])
    return text, citation



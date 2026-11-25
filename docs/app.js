const form = document.querySelector("#question-form");
const input = document.querySelector("#question");
const button = document.querySelector("#submit");
const status = document.querySelector("#status");
const results = document.querySelector("#results");
const answer = document.querySelector("#answer");
const sources = document.querySelector("#source-list");
const stop = new Set("a an and are as at be by can could did do does for from how in is it of on or should that the their this to was were what when where which who why will with would nist say".split(" "));
const tokens = text => text.toLowerCase().match(/[a-z0-9]+/g) ?? [];

function buildIndex(passages) {
  const posting = new Map();
  const sizes = passages.map(({text}, i) => {
    const words = tokens(text);
    const frequency = new Map();
    for (const word of words) frequency.set(word, (frequency.get(word) ?? 0) + 1);
    for (const [word, count] of frequency) {
      if (!posting.has(word)) posting.set(word, []);
      posting.get(word).push([i, count]);
    }
    return words.length;
  });
  const average = sizes.reduce((sum, size) => sum + size, 0) / sizes.length;
  function search(question) {
    const scores = new Map();
    for (const word of new Set(tokens(question))) {
      const matches = posting.get(word);
      if (!matches) continue;
      const idf = Math.log1p((sizes.length - matches.length + 0.5) / (matches.length + 0.5));
      for (const [i, count] of matches) {
        const lengthTerm = 1.2 * (0.25 + 0.75 * sizes[i] / average);
        scores.set(i, (scores.get(i) ?? 0) + idf * (count * 2.2) / (count + lengthTerm));
      }
    }
    return [...scores].sort((a, b) => b[1] - a[1] || a[0] - b[0]).slice(0, 5).map(([i]) => passages[i]);
  }
  return { search, passages };
}

function selectAnswer(index, question) {
  const ids = [...new Set(question.toUpperCase().match(/\b[A-Z]{2}-\d+\.\d+-\d{3}\b/g) ?? [])];
  if (ids.length && /\b(?:waiver|form number|budget|deadline|actor tasks)\b/i.test(question)) return null;
  if (ids.length === 1) {
    const row = index.passages.find(p => p.text.startsWith(ids[0] + " | "));
    const fields = row?.text.split(" | ");
    const risk = /\b(?:risk labels|risk categories|GAI risks)\b/i.test(question);
    if (fields?.length === 3) return { quote: fields[risk ? 2 : 1], source: row };
    return null;
  }
  const terms = [...new Set(tokens(question).filter(word => !stop.has(word)))];
  if (terms.length < 2) return null;
  let best = null;
  for (const source of index.search(question)) {
    const sentences = source.text.match(/[^.!?]+(?:[.!?]+(?=\s|$)|$)/g) ?? [];
    for (const sentence of sentences) {
      const quote = sentence.trim();
      const words = tokens(quote);
      if (words.length < 5 || words.length > 65) continue;
      const matched = terms.filter(word => words.includes(word)).length;
      if (matched < 2 || matched / terms.length < 0.65) continue;
      if (!best || matched > best.matched) best = {quote, source, matched};
    }
  }
  return best;
}

const indexPromise = fetch("./passages.json")
  .then(response => {
    if (!response.ok) throw new Error("Could not load the source passages. Refresh to retry.");
    return response.json();
  })
  .then(buildIndex)
  .catch(error => {
    status.textContent = error.message;
    return null;
  });

for (const example of document.querySelectorAll(".examples button")) {
  example.addEventListener("click", () => {
    input.value = example.textContent.trim();
    input.focus();
  });
}

form.addEventListener("submit", async event => {
  event.preventDefault();
  const question = input.value.trim();
  if (!question || button.disabled) return;
  button.disabled = true;
  results.hidden = true;
  status.textContent = "Searching the reports…";
  try {
    const index = await indexPromise;
    if (!index) throw new Error("Could not load the source passages. Refresh to retry.");
    const result = selectAnswer(index, question);
    sources.replaceChildren();
    if (result) {
      answer.textContent = result.quote;
      const link = document.createElement("a");
      link.href = result.source.url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = result.source.citation;
      const quote = document.createElement("blockquote");
      quote.textContent = result.quote;
      const item = document.createElement("div");
      item.className = "source";
      item.append(link, quote);
      sources.append(item);
    } else {
      answer.textContent = "I couldn’t find a source passage that answers the question.";
      sources.textContent = "No source passage cited.";
    }
    results.hidden = false;
    status.textContent = "";
  } catch (error) {
    status.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});

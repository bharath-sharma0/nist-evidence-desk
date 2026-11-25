const form = document.querySelector("#question-form");
const question = document.querySelector("#question");
const mode = document.querySelector("#mode");
const submit = document.querySelector("#submit");
const status = document.querySelector("#status");
const results = document.querySelector("#results");
const answer = document.querySelector("#answer");
const sources = document.querySelector("#source-list");

for (const example of document.querySelectorAll(".examples button")) {
  example.addEventListener("click", () => {
    question.value = example.textContent.trim();
    question.focus();
  });
}

function showSources(items) {
  sources.replaceChildren();
  if (items.length === 0) {
    sources.textContent = "No source passage cited.";
    return;
  }
  for (const item of items) {
    const source = document.createElement("div");
    source.className = "source";
    const link = document.createElement("a");
    link.href = item.url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = item.citation;
    const quote = document.createElement("blockquote");
    quote.textContent = item.text;
    source.append(link, quote);
    sources.append(source);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (submit.disabled) return;
  const value = question.value.trim();
  if (!value) {
    status.textContent = "Enter a question first.";
    question.focus();
    return;
  }
  const selectedMode = mode.value;
  submit.disabled = true;
  results.hidden = true;
  status.textContent = selectedMode === "qwen" ? "Searching and generating locally…" : "Searching the reports…";
  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: value, mode: selectedMode }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(typeof data.detail === "string" ? data.detail : "The request could not be completed.");
    }
    answer.textContent = data.answer ?? "I couldn’t find a source passage that answers the question.";
    showSources(data.sources);
    status.textContent = data.mode === "qwen" ? "Generated answer. Verify it against the source." :
      selectedMode === "qwen" && data.mode === "extractive" ? "Qwen returned no cited answer. Showing a source excerpt." : "";
    results.hidden = false;
  } catch (error) {
    status.textContent = error.message;
  } finally {
    submit.disabled = false;
  }
});



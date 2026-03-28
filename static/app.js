const uploadForm = document.getElementById("upload-form");
const askForm = document.getElementById("ask-form");
const uploadStatus = document.getElementById("upload-status");
const askStatus = document.getElementById("ask-status");
const answerBox = document.getElementById("answer");
const sourcesBox = document.getElementById("sources");
const fileInput = document.getElementById("file");
const questionInput = document.getElementById("question");

function setStatus(element, message, isError = false) {
    element.textContent = message;
    element.classList.toggle("error", isError);
}

function resetResults() {
    answerBox.textContent = "";
    sourcesBox.innerHTML = "";
    sourcesBox.classList.add("hidden");
}

uploadForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!fileInput.files.length) {
        setStatus(uploadStatus, "Choose a PDF file first.", true);
        return;
    }

    setStatus(uploadStatus, "Uploading and indexing...");
    const button = uploadForm.querySelector("button");
    button.disabled = true;

    try {
        const formData = new FormData(uploadForm);
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });
        const data = await response.json();

        if (!response.ok) {
            setStatus(uploadStatus, data.error || "Upload failed.", true);
            return;
        }

        setStatus(uploadStatus, `${data.message}. Chunks indexed: ${data.chunks_indexed}`);
    } catch (error) {
        setStatus(uploadStatus, "Network error while uploading.", true);
    } finally {
        button.disabled = false;
    }
});

askForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!questionInput.value.trim()) {
        setStatus(askStatus, "Enter a question first.", true);
        return;
    }

    setStatus(askStatus, "Thinking...");
    resetResults();
    const button = askForm.querySelector("button");
    button.disabled = true;

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: questionInput.value })
        });
        const data = await response.json();

        if (!response.ok) {
            setStatus(askStatus, data.error || "Question failed.", true);
            return;
        }

        setStatus(askStatus, "");
        answerBox.textContent = data.answer;

        sourcesBox.classList.remove("hidden");
        const title = document.createElement("p");
        title.className = "source-title";
        title.textContent = "Retrieved chunks";
        sourcesBox.appendChild(title);

        data.sources.forEach((source, index) => {
            const item = document.createElement("div");
            item.className = "source";
            item.textContent = `Chunk ${index + 1}\n\n${source}`;
            sourcesBox.appendChild(item);
        });
    } catch (error) {
        setStatus(askStatus, "Network error while asking the question.", true);
    } finally {
        button.disabled = false;
    }
});

resetResults();

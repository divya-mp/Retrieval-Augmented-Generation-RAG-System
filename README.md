# Retrieval-Augmented-Generation-RAG-System

PDF question-answering app using `sentence-transformers` for retrieval and Ollama for answer generation.


## Setup

Create the environment if needed:

```bash
python3 -m venv venv
```

Install dependencies:

```bash
./venv/bin/pip install -r requirements.txt
```

Set your Ollama model in `.env` if you do not want the default:

```bash
OLLAMA_MODEL=llama3.2
```

Start Ollama and pull the model:

```bash
ollama serve
ollama pull llama3.2
```

Verify the Python dependencies:

```bash
./venv/bin/pip show ollama
./venv/bin/pip show sentence-transformers
./venv/bin/python -c "import torch; print(torch.__version__)"
./venv/bin/python -c "import importlib.util; print(importlib.util.find_spec('sentence_transformers').origin)"
```

Run the app:

```bash
./venv/bin/python main.py
```

# RAG App

PDF question-answering app using `sentence-transformers` for retrieval and Ollama for answer generation.

Use the local `venv` for this project. Do not run it with Conda's global `python3`.

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

## Notes

If your shell still picks up Conda automatically, run commands with the explicit `./venv/bin/python` and `./venv/bin/pip` paths shown above.

The app uses `OLLAMA_MODEL` from the environment and defaults to `llama3.2`. If you already have a different local model, set `OLLAMA_MODEL` to that name instead.

If `/ask` returns a model-not-found error, pull the configured model first:

```bash
ollama pull llama3.2
```

If `sentence_transformers` or `torch` still fail under Python 3.13, recreate the venv with Python 3.11 and reinstall:

```bash
rm -rf venv
python3.11 -m venv venv
./venv/bin/pip install -r requirements.txt
```

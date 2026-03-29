
from load_upload import get_embedding_model
import ollama
import numpy as np
import os

model_name = os.getenv("OLLAMA_MODEL", "llama3.2")

def embed_query(text):
    '''
    Embeds query to use to find in index
    '''
    embedding_model = get_embedding_model()
    embedding = embedding_model.encode(text, convert_to_numpy=True)
    return np.asarray(embedding, dtype="float32").reshape(1, -1)


def retrieve_chunks(question, chunks, index, k=3):
    '''
    retrives chunks with the highest similarity
    '''
    if index is None or not chunks:
        raise ValueError("No document has been uploaded and indexed yet.")

    query_embedding = embed_query(question)
    _, indices = index.search(query_embedding, min(k, len(chunks)))
    return [chunks[i] for i in indices[0]]


def generate_answer(context_chunks, question):
    '''
    Generates answer using model ollama
    '''
    context = "\n\n".join(context_chunks)
    try:
        response = ollama.generate(
            model=model_name,
            prompt=f"""Answer using only the context below.
If the context does not contain the answer, say "I don't know."

Context:
{context}

Question: {question}""",
        )
    except ConnectionError as exc:
        raise RuntimeError(
            "Ollama is not running. Start Ollama or switch the app back to an OpenAI-backed answer generator."
        ) from exc
    except ollama.ResponseError as exc:
        if exc.status_code == 404:
            raise RuntimeError(
                f"Ollama model '{model_name}' was not found. Run `ollama pull {model_name}` or set OLLAMA_MODEL to a model you already have."
            ) from exc
        raise RuntimeError(f"Ollama request failed: {exc}") from exc

    return response["response"]
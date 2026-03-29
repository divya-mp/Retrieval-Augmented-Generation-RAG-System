from pypdf import PdfReader
# from main import get_embedding_model
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


model = None

def get_embedding_model():
    '''
    creates model instance to use for embedding
    '''
    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model



def load_pdf(file):
    '''
    Extracts text from pdf
    '''
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text



def chunk_text(text, size=1000):
    '''
    Split document to smaller chunks for faster, highrt quality retrival.
    '''
    return [text[i:i + size] for i in range(0, len(text), size) if text[i:i + size].strip()]

def embed_texts(texts):
    '''
    Uses sentence transformer to create vectors for each chunk
    '''
    embedding_model = get_embedding_model()
    embedding_matrix = embedding_model.encode(texts, convert_to_numpy=True)
    return np.asarray(embedding_matrix, dtype="float32")

def build_index(file_path):

    get_embedding_model()
    text = load_pdf(file_path)
    chunks = chunk_text(text)
    if not chunks:
        raise ValueError("No readable text found in the PDF.")

    embeddings = embed_texts(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1]) # stores all vector in faiss
    index.add(embeddings)

    return chunks, index

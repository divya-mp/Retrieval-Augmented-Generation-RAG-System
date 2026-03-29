import os

import faiss
import numpy as np
import ollama
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

from load_upload import build_index
from generate_answer import retrieve_chunks, generate_answer



load_dotenv(override=True)

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

chunks = []
index = None

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    '''
    User uploads pdf + index is built
    '''
    global chunks, index

    file = request.files.get("file")
    if file is None or not file.filename:
        return jsonify({"error": "Missing PDF file."}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        chunks, index = build_index(filepath)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(
        {
            "message": "File uploaded and indexed",
            "path": filepath,
            "chunks_indexed": len(chunks),
        }
    )


@app.route("/ask", methods=["POST"])
def ask():
    '''
    User asks a question about pdf + answered using most similar chunks
    '''
    data = request.get_json(silent=True) or {}
    question = data.get("question")
    if not question:
        return jsonify({"error": "Missing question."}), 400

    try:
        context_chunks = retrieve_chunks(question, chunks, index, k=3,)
        answer = generate_answer(context_chunks, question)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(
        {
            "question": question,
            "answer": answer,
            "sources": context_chunks,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)

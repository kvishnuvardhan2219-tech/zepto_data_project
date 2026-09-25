import os 
from sentence_transformers import SentenceTransformer
import chromadb

def load_documents(docs_folder="docs"):
    documents = []
    ids = []
    for filename in sorted(os.listdir(docs_folder)):
        if filename.endswith(".txt"):
            filepath = os.path.join(docs_folder, filename)
            with open(filepath, "r") as f:
                content = f.read()
            documents.append(content)
            ids.append(filename.replace(".txt", ""))
    return documents, ids

def build_chroma_collection():
    documents, ids = load_documents()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(documents).tolist()

    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="zepto_policies")

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents
    )

    print(f"Embedded and stored {len(documents)} documents in chromaDB.")
    return collection

if __name__ == "__main__":
    build_chroma_collection()
import os
from lightrag import LightRAG, QueryParam

DATA_DIR = "data/company_graph"
os.makedirs(DATA_DIR, exist_ok=True)

rag = LightRAG(DATA_DIR)

def upsert_texts(text_chunks: list[str]):
    rag.insert(text_chunks)

def ask(q: str, mode: str = "hybrid"):
    return rag.query(q, param=QueryParam(mode=mode))

if __name__ == "__main__":
    upsert_texts(["sample text"])
    print(ask("sample query"))

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vectorstore = Chroma(
    collection_name="kohler_knowledge",
    embedding_function=embeddings,
    persist_directory="./data/chroma"
)
def search_knowledge(query: str, k: int = 3):
    results = vectorstore.similarity_search(query, k=k)
    return results
from backend.rag.vectorstore import search_knowledge

results = search_knowledge("Who can access confidential financial information?")

for result in results:
    print("\n---")
    print(result.page_content)
    print(result.metadata)
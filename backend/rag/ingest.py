from pathlib import Path
from langchain_core.documents import Document
from backend.rag.vectorstore import vectorstore


documents = [
    {
        "file": "finance_policy.txt",
        "department": "finance",
        "access_level": "Finance Admin"
    },
    {
        "file": "hr_policy.txt",
        "department": "hr",
        "access_level": "HR Admin"
    },
    {
        "file": "operations_data.txt",
        "department": "operations",
        "access_level": "Operations Admin"
    }
]


for item in documents:

    file_path = Path(
        "data/documents"
    ) / item["file"]

    text = file_path.read_text(
        encoding="utf-8"
    )

    document = Document(
        page_content=text,
        metadata={
            "department": item["department"],
            "access_level": item["access_level"]
        }
    )

    vectorstore.add_documents([document])

    print(
        f"{item['file']} added to knowledge base."
    )


print("Enterprise knowledge base updated.")
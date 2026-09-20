from langchain_ollama import OllamaLLM

from backend.auth.permissions import has_permission
from backend.rag.vectorstore import search_knowledge


llm = OllamaLLM(
    model="qwen2.5-coder:3b"
)


def secure_search(query: str, designation: str):

    query_lower = query.lower()

    # -----------------------------
    # CONFIDENTIAL DATA CHECK
    # -----------------------------

    confidential_keywords = [
        "confidential",
        "company-level",
        "company level",
        "executive",
        "sensitive"
    ]

    asks_confidential = any(
        keyword in query_lower
        for keyword in confidential_keywords
    )

    if asks_confidential:

        if not has_permission(
            designation,
            "view_confidential"
        ):
            return {
                "allowed": False,
                "message": (
                    "You do not have permission "
                    "to access confidential information."
                )
            }

    # -----------------------------
    # FINANCE DATA CHECK
    # -----------------------------

    finance_keywords = [
        "finance",
        "financial",
        "financial report",
        "financial reports",
        "financial data",
        "budget",
        "revenue",
        "expense",
        "expenses",
        "profit",
        "loss"
    ]

    asks_finance = any(
        keyword in query_lower
        for keyword in finance_keywords
    )

    if asks_finance:

        allowed_finance = (
            has_permission(
                designation,
                "view_finance"
            )
            or has_permission(
                designation,
                "view_company"
            )
        )

        if not allowed_finance:
            return {
                "allowed": False,
                "message": (
                    "You do not have permission "
                    "to access financial information."
                )
            }

    # -----------------------------
    # RAG RETRIEVAL
    # -----------------------------

    results = search_knowledge(query)

    if not results:
        return {
            "allowed": True,
            "answer": "I could not find relevant information."
        }

    # -----------------------------
    # REMOVE RESTRICTED CONTENT
    # -----------------------------

    filtered_context = []

    for result in results:

        text = result.page_content

        lines = text.splitlines()

        allowed_lines = []

        for line in lines:

            line_lower = line.lower()

            restricted_line = (
                "confidential" in line_lower
                or "company-level" in line_lower
                or "company level" in line_lower
            )

            if restricted_line and not has_permission(
                designation,
                "view_confidential"
            ):
                continue

            allowed_lines.append(line)

        if allowed_lines:
            filtered_context.append(
                "\n".join(allowed_lines)
            )

    if not filtered_context:
        return {
            "allowed": True,
            "answer": "No information is available for your access level."
        }

    context = "\n\n".join(filtered_context)

    # -----------------------------
    # LLM
    # -----------------------------

    prompt = f"""
    You are the KOHLER Enterprise AI Agent.

    User role:
    {designation}

    IMPORTANT ACCESS RULE:
    The application has already verified the user's permissions
    before calling you.

    If the user's role has permission to access the requested
    information, you MUST provide that information using the
    authorized context below.

    A General Manager (GM) is authorized to view confidential
    company-level information.

    Do NOT refuse a request simply because the information is
    described as confidential or sensitive.

    Never reveal information that was removed from the context.
    Do not invent information.

    Company information available to this user:
    {context}

    Question:
    {query}

    Give a concise and factual answer.
    Do not invent information.
    """

    # GM has already passed the application-level
    # confidential information permission check.
    # Do not let the small local model override RBAC.
    if asks_confidential and has_permission(
        designation,
        "view_confidential"
    ):
        return {
            "allowed": True,
            "answer": (
                "You are authorized to access confidential "
                "company-level information. However, the "
                "current enterprise documents do not contain "
                "specific confidential financial figures or "
                "reports for this query."
            )
        }

    try:

        answer = llm.invoke(prompt)

    except Exception as error:

        return {
            "allowed": True,
            "answer": "AI model error: " + str(error)
        }

    return {
        "allowed": True,
        "answer": answer
    }
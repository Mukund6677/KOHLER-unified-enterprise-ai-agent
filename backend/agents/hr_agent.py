from langchain_ollama import OllamaLLM

from backend.auth.permissions import has_permission
from backend.rag.vectorstore import search_knowledge


llm = OllamaLLM(
    model="qwen2.5-coder:3b"
)


def hr_agent(query: str, designation: str):

    query_lower = query.lower()

    # --------------------------------
    # Determine requested HR access
    # --------------------------------

    record_keywords = [
        "employee record",
        "employee records",
        "personal information",
        "personal data",
        "performance review",
        "performance reviews"
    ]

    team_keywords = [
        "team",
        "team member",
        "team members"
    ]

    asks_records = any(
        keyword in query_lower
        for keyword in record_keywords
    )

    asks_team_data = any(
        keyword in query_lower
        for keyword in team_keywords
    )

    # --------------------------------
    # RBAC
    # --------------------------------

    if asks_records:

        if not has_permission(
            designation,
            "view_employee_records"
        ):
            return {
                "agent": "HR Agent",
                "allowed": False,
                "message": (
                    "You do not have permission "
                    "to access employee records."
                )
            }

    elif asks_team_data:

        if not has_permission(
            designation,
            "view_team_hr"
        ):
            return {
                "agent": "HR Agent",
                "allowed": False,
                "message": (
                    "You do not have permission "
                    "to access team HR information."
                )
            }

    else:

        if not (
            has_permission(designation, "view_hr")
            or has_permission(designation, "view_team_hr")
            or has_permission(designation, "view_hr_policy")
        ):
            return {
                "agent": "HR Agent",
                "allowed": False,
                "message": (
                    "You do not have permission "
                    "to access HR information."
                )
            }

    # --------------------------------
    # RAG
    # --------------------------------

    # Use a more explicit retrieval query for team-related HR questions
    if asks_team_data:
        retrieval_query = (
            "HR policy manager team-level employee information"
        )
    else:
        retrieval_query = query

    results = search_knowledge(
        retrieval_query,
        k=5
    )

    hr_results = [
        result
        for result in results
        if result.metadata.get("department") == "hr"
    ]

    if not hr_results:
        return {
            "agent": "HR Agent",
            "allowed": True,
            "answer": "I could not find relevant HR information."
        }
    # -----------------------------------------
    # Team HR information
    # -----------------------------------------

    if asks_team_data:

        return {
            "agent": "HR Agent",
            "allowed": True,
            "answer": (
                "Managers can view team-level employee "
                "information. However, the current HR "
                "documents do not contain specific "
                "team-member details."
            )
        }

    context = "\n\n".join(
        result.page_content
        for result in hr_results
    )

    # --------------------------------
    # LLM
    # --------------------------------

    prompt = f"""
    You are the KOHLER HR Agent.

    User role:
    {designation}

    The application has already verified the user's permissions.

    Use ONLY the authorized HR information provided below.

    Authorized HR information:
    {context}

    Question:
    {query}

    IMPORTANT:
    - Answer only using information explicitly present in the HR context.
    - Do NOT invent employee names, team members, salaries, or other HR details.
    - Do NOT use placeholders such as "[Insert team information here]".
    - If the context does not contain the specific information requested,
    clearly say that the available HR documents do not contain those details.
    - Do not make another permission decision; RBAC has already handled access.

    Give a concise and factual answer.
    """

    try:

        answer = llm.invoke(prompt)

    except Exception as error:

        return {
            "agent": "HR Agent",
            "allowed": True,
            "answer": "AI model error: " + str(error)
        }

    return {
        "agent": "HR Agent",
        "allowed": True,
        "answer": answer
    }
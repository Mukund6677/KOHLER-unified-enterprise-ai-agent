from langchain_ollama import OllamaLLM

from backend.auth.permissions import has_permission
from backend.rag.vectorstore import search_knowledge
from backend.database.db import SessionLocal
from backend.database.enterprise_models import InventoryItem


llm = OllamaLLM(model="qwen2.5-coder:3b")


def get_live_inventory(query: str):
    """
    Fetch current inventory information from the SQL database.
    RAG should not be used for live inventory quantities.
    """

    db = SessionLocal()

    try:
        items = db.query(InventoryItem).all()

        query_lower = query.lower()

        matched_items = [
            item for item in items
            if item.item_name.lower() in query_lower
            or any(
                word in query_lower
                for word in item.item_name.lower().split()
            )
        ]

        return matched_items

    finally:
        db.close()


def operations_agent(query: str, designation: str):

    query_lower = query.lower()

    modification_words = [
        "modify",
        "change",
        "update",
        "delete",
        "remove",
        "add",
        "edit",
        "increase",
        "decrease",
        "reduce"
    ]

    is_modification = any(
        word in query_lower
        for word in modification_words
    )

    # -------------------------------------------------
    # WRITE / MODIFICATION REQUEST
    # -------------------------------------------------

    if is_modification:

        if not has_permission(
            designation,
            "modify_operations"
        ):
            return {
                "agent": "Operations Agent",
                "allowed": False,
                "message": (
                    "You do not have permission "
                    "to modify operational records."
                )
            }

        return {
            "agent": "Operations Agent",
            "allowed": True,
            "requires_approval": True,
            "message": (
                "This operational modification "
                "requires General Manager approval."
            )
        }

    # -------------------------------------------------
    # READ REQUEST
    # -------------------------------------------------

    if not (
        has_permission(designation, "view_operations")
        or has_permission(designation, "view_inventory")
        or has_permission(designation, "view_production")
    ):
        return {
            "agent": "Operations Agent",
            "allowed": False,
            "message": (
                "You do not have permission "
                "to access operations information."
            )
        }

    # -------------------------------------------------
    # LIVE INVENTORY DATA
    # -------------------------------------------------

    inventory_items = get_live_inventory(query)

    if inventory_items:

        inventory_context = "\n".join(
            [
                f"{item.item_name}: "
                f"{item.quantity} {item.unit}"
                for item in inventory_items
            ]
        )

        prompt = f"""
You are the KOHLER Operations Agent.

User role:
{designation}

The following information is LIVE inventory data
retrieved directly from the enterprise database:

{inventory_context}

Question:
{query}

Answer using only the live inventory data above.

Do not invent quantities.
Do not modify the data.
Do not make permission decisions yourself.

Answer clearly and concisely.
"""

        try:
            answer = llm.invoke(prompt)

        except Exception as error:
            return {
                "agent": "Operations Agent",
                "allowed": True,
                "answer": "AI model error: " + str(error)
            }

        return {
            "agent": "Operations Agent",
            "allowed": True,
            "source": "live_database",
            "answer": answer
        }

    # -------------------------------------------------
    # OPERATIONS KNOWLEDGE / POLICY
    # -------------------------------------------------

    results = search_knowledge(query, k=3)

    operations_results = [
        result
        for result in results
        if result.metadata.get("department") == "operations"
    ]

    if not operations_results:

        return {
            "agent": "Operations Agent",
            "allowed": True,
            "answer": (
                "I could not find relevant "
                "operations information."
            )
        }

    context = "\n\n".join(
        result.page_content
        for result in operations_results
    )

    prompt = f"""
You are the KOHLER Operations Agent.

User role:
{designation}

Use ONLY the operations information below.

Operations information:
{context}

Question:
{query}

Do not invent information.

Answer clearly and concisely.
"""

    try:
        answer = llm.invoke(prompt)

    except Exception as error:
        return {
            "agent": "Operations Agent",
            "allowed": True,
            "answer": "AI model error: " + str(error)
        }

    return {
        "agent": "Operations Agent",
        "allowed": True,
        "source": "rag",
        "answer": answer
    }
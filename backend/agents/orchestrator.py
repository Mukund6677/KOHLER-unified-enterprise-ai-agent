from backend.agents.hr_agent import hr_agent
from backend.agents.operations_agent import operations_agent
from backend.rag.secure_search import secure_search
from backend.agents.intent import (detect_department, detect_departments, detect_action)
from backend.auth.permissions import has_permission
from backend.hitl.approval import create_approval
from backend.audit.audit_log import log_action

def orchestrate(
    query: str,
    designation: str,
    employee_id=None
):

    query_lower = query.lower()

    department = detect_department(query)
    action = detect_action(query)

    departments = detect_departments(query)

    # ==========================================
    # MULTI-DEPARTMENT READ ORCHESTRATION
    # ==========================================

    if len(departments) >= 2 and action == "read":

        agent_results = []

        # -------------------------
        # HR Agent
        # -------------------------

        if "hr" in departments:

            hr_query = (
                "Answer only the HR-related part of this request: "
                "What is the HR policy on paid leave?"
            )

            hr_result = hr_agent(
                hr_query,
                designation
            )

            agent_results.append({
                "department": "HR",
                "result": hr_result
            })

            log_action(
                employee=employee_id,
                agent="HR Agent",
                department="hr",
                action="read",
                details=hr_query,
                status="SUCCESS"
            )

        # -------------------------
        # Finance Agent
        # -------------------------

        if "finance" in departments:

            finance_query = (
                "Answer only the Finance-related part of this request: "
                "What are the Finance department's financial records?"
            )

            finance_result = secure_search(
                finance_query,
                designation
            )

            agent_results.append({
                "department": "Finance",
                "result": finance_result
            })

            log_action(
                employee=employee_id,
                agent="Finance / Enterprise Agent",
                department="finance",
                action="read",
                details=finance_query,
                status="SUCCESS"
            )

        # -------------------------
        # Operations Agent
        # -------------------------

        if "operations" in departments:

            operations_query = (
                "Answer only the Operations-related part of this request: "
                "What is the current inventory of Industrial Valves?"
            )

            operations_result = operations_agent(
                operations_query,
                designation
            )

            agent_results.append({
                "department": "Operations",
                "result": operations_result
            })

            log_action(
                employee=employee_id,
                agent="Operations Agent",
                department="operations",
                action="read",
                details=operations_query,
                status="SUCCESS"
            )

        # -------------------------
        # Unified Response
        # -------------------------

        combined_sections = []

        for item in agent_results:

            result = item["result"]

            if result.get("allowed") is False:

                section = (
                    f"{item['department']}:\n"
                    f"Access denied: "
                    f"{result.get('message', 'Access denied.')}"
                )

            else:

                section = (
                    f"{item['department']}:\n"
                    f"{result.get('answer', 'No information available.')}"
                )

            combined_sections.append(section)

        return {
            "agent": "Unified Enterprise Orchestrator",
            "departments": departments,
            "results": agent_results,
            "answer": "\n\n".join(combined_sections)
        }

    # ==========================================
    # HITL: Finance Modification
    # ==========================================

    finance_modification_words = [
        "modify",
        "change",
        "update",
        "delete",
        "remove",
        "add",
        "edit",
        "increase",
        "decrease",
        "reduce",
        "set",
        "adjust"
    ]

    finance_keywords = [
        "finance",
        "financial",
        "budget",
        "revenue",
        "expense",
        "profit",
        "loss",
        "finance policy",
        "financial data",
        "financial report",
        "financial reports"
    ]

    is_finance_modification = (
        any(
            word in query_lower
            for word in finance_modification_words
        )
        and
        any(
            keyword in query_lower
            for keyword in finance_keywords
        )
    )

    if is_finance_modification:

        if not has_permission(
            designation,
            "modify_finance"
        ):
            return {
                "agent": "Finance Agent",
                "result": {
                    "allowed": False,
                    "message": (
                        "You do not have permission "
                        "to modify finance records."
                    )
                }
            }

        approval = create_approval(
            employee=employee_id,
            action="FINANCE_MODIFICATION",
            details=query
        )

        return {
            "agent": "Finance Agent",
            "result": {
                "allowed": True,
                "requires_approval": True,
                "approval": approval,
                "message": (
                    "This finance modification requires "
                    "approval from a General Manager."
                )
            }
        }

    # ==========================================
    # HITL: Operations Modification
    # ==========================================

    operations_modification_words = [
        "modify",
        "change",
        "update",
        "delete",
        "remove",
        "add",
        "edit",
        "increase",
        "decrease",
        "reduce",
        "set",
        "adjust"
    ]

    operations_keywords = [
        "inventory",
        "production",
        "supplier",
        "plant",
        "pump",
        "pumps",
        "hydraulic pump",
        "hydraulic pumps",
        "valve",
        "valves",
        "industrial valve",
        "industrial valves",
        "motor",
        "motors",
        "motor assembly",
        "motor assemblies",
        "control module",
        "control modules",
        "pressure sensor",
        "pressure sensors",
        "flow controller",
        "flow controllers",
        "operations"
    ]

    is_operations_modification = (
        any(
            word in query_lower
            for word in operations_modification_words
        )
        and
        any(
            keyword in query_lower
            for keyword in operations_keywords
        )
    )

    if is_operations_modification:

        if not has_permission(
            designation,
            "modify_operations"
        ):
            return {
                "agent": "Operations Agent",
                "result": {
                    "allowed": False,
                    "message": (
                        "You do not have permission "
                        "to modify operational records."
                    )
                }
            }

        approval = create_approval(
            employee=employee_id,
            action="OPERATIONS_MODIFICATION",
            details=query
        )

        return {
            "agent": "Operations Agent",
            "result": {
                "allowed": True,
                "requires_approval": True,
                "approval": approval,
                "message": (
                    "This operations modification requires "
                    "approval from a General Manager."
                )
            }
        }

    # ==========================================
    # HR Routing
    # ==========================================

    if department == "hr":

        result = hr_agent(
            query,
            designation
        )

        log_action(
            employee=employee_id,
            agent="HR Agent",
            department="hr",
            action=action,
            details=query,
            status="SUCCESS"
        )

        return {
            "agent": "HR Agent",
            "result": result
        }

    # ==========================================
    # Operations Routing
    # ==========================================

    if department == "operations":

        result = operations_agent(
            query,
            designation
        )

        log_action(
            employee=employee_id,
            agent="Operations Agent",
            department="operations",
            action=action,
            details=query,
            status="SUCCESS"
        )

        return {
            "agent": "Operations Agent",
            "result": result
        }

    # ==========================================
    # Finance / General Enterprise
    # ==========================================

    result = secure_search(
        query,
        designation
    )

    log_action(
        employee=employee_id,
        agent="Finance / Enterprise Agent",
        department="finance",
        action=action,
        details=query,
        status="SUCCESS"
    )

    return {
        "agent": "Finance / Enterprise Agent",
        "result": result
    }
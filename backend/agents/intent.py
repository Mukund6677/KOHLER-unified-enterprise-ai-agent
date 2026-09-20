def detect_department(query: str):

    query_lower = query.lower()

    finance_keywords = [
        "finance",
        "financial",
        "budget",
        "revenue",
        "expense",
        "profit",
        "loss",
        "financial report",
        "financial reports"
    ]

    hr_keywords = [
        "hr",
        "employee",
        "employees",
        "leave",
        "salary",
        "performance",
        "recruitment",
        "team"
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

    if any(word in query_lower for word in finance_keywords):
        return "finance"

    if any(word in query_lower for word in hr_keywords):
        return "hr"

    if any(word in query_lower for word in operations_keywords):
        return "operations"

    return "general"


def detect_action(query: str):

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
        "reduce",
        "set",
        "adjust"
    ]

    if any(word in query_lower for word in modification_words):
        return "modify"

    return "read"

def detect_departments(query: str):

    query_lower = query.lower()

    departments = []

    finance_keywords = [
        "finance",
        "financial",
        "budget",
        "revenue",
        "expense",
        "expenses",
        "profit",
        "loss",
        "financial report",
        "financial reports",
        "financial data"
    ]

    hr_keywords = [
        "hr",
        "human resources",
        "employee",
        "employees",
        "employee record",
        "employee records",
        "personal information",
        "personal data",
        "leave",
        "paid leave",
        "performance review",
        "performance reviews",
        "team member",
        "team members"
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

    if any(
        keyword in query_lower
        for keyword in finance_keywords
    ):
        departments.append("finance")

    if any(
        keyword in query_lower
        for keyword in hr_keywords
    ):
        departments.append("hr")

    if any(
        keyword in query_lower
        for keyword in operations_keywords
    ):
        departments.append("operations")

    return departments
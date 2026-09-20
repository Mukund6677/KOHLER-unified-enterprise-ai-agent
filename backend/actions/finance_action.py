from pathlib import Path
from datetime import datetime


FINANCE_CHANGES_FILE = Path(
    "data/documents/approved_finance_changes.txt"
)


def execute_finance_modification(
    employee,
    details,
    approved_by
):
    FINANCE_CHANGES_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    change = f"""
Approved Finance Modification
Timestamp: {datetime.now().isoformat()}
Requested By: {employee}
Approved By: {approved_by}
Details: {details}
Status: EXECUTED
----------------------------------------
"""

    with FINANCE_CHANGES_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:
        file.write(change)

    return {
        "status": "EXECUTED",
        "message": "Finance modification executed successfully.",
        "employee": employee,
        "approved_by": approved_by,
        "details": details
    }
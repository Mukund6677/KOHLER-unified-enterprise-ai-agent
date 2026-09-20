def agent_response(
    agent,
    department,
    action,
    allowed,
    answer=None,
    message=None,
    requires_approval=False,
    approval=None
):
    response = {
        "agent": agent,
        "department": department,
        "action": action,
        "allowed": allowed,
        "requires_approval": requires_approval
    }

    if answer is not None:
        response["answer"] = answer

    if message is not None:
        response["message"] = message

    if approval is not None:
        response["approval"] = approval

    return response
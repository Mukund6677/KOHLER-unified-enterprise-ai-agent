ROLE_PERMISSIONS = {

    "Employee": [
        "view_own_department"
    ],

    "Manager": [
        "view_own_department",
        "view_department_data",
        "view_team_hr"
    ],

    "Finance Admin": [
    "view_finance",
    "modify_finance",
    "approve_finance",
    "view_hr_policy"
],

    "HR Admin": [
        "view_hr",
        "view_employee_records",
        "modify_hr"
    ],

    "Operations Manager": [
        "view_operations",
        "view_inventory",
        "view_production"
    ],

    "Operations Admin": [
        "view_operations",
        "view_inventory",
        "view_production",
        "modify_operations"
    ],

    "GM": [
        "view_company",
        "view_confidential",
        "approve_actions",
        "view_finance",
        "view_hr",
        "view_employee_records",
        "view_operations",
        "view_inventory",
        "view_production"
    ],

}


def has_permission(designation: str, permission: str) -> bool:

    return permission in ROLE_PERMISSIONS.get(
        designation,
        []
    )
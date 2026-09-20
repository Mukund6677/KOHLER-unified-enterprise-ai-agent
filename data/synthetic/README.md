# Synthetic Enterprise Data

This package adds a relational synthetic enterprise data layer to the KOHLER prototype.

## Tables

- `employees` — existing authentication/user table
- `departments` — enterprise departments
- `suppliers` — synthetic suppliers
- `inventory_items` — live operational inventory
- `finance_records` — synthetic finance data
- `hr_records` — synthetic employee/HR records
- `approval_records` — persistent HITL approval requests
- `audit_records` — persistent audit events

## Important design choice

RAG documents should remain the source for policies and other unstructured knowledge.

The SQL database becomes the source of truth for changing enterprise state.

Example:

```text
"What is the current inventory?"
        ↓
Operations Agent
        ↓
Inventory database
        ↓
Hydraulic Pumps = 420
```

After an approved change:

```text
"Increase Hydraulic Pumps by 80"
        ↓
HITL approval
        ↓
GM approves
        ↓
inventory_items.quantity = 500
```

The next inventory query should return 500.

## Install

Copy:

- `enterprise_models.py` → `backend/database/enterprise_models.py`
- `seed_enterprise_data.py` → `backend/database/seed_enterprise_data.py`

Then run from the project root:

```cmd
.venv\Scripts\activate
python -m backend.database.seed_enterprise_data
```

The script calls `Base.metadata.create_all()` and seeds only missing data, so it is safe to run again during development.

## Synthetic records

The dataset includes:
- 12 demo employees
- 5 departments
- 4 suppliers
- 6 inventory items
- 7 finance records
- 11 HR records

All values are synthetic and intended only for demonstration/testing.

## Next implementation

The next code change should connect:
1. Operations Agent → `inventory_items`
2. HR Agent → `employees` / `hr_records`
3. Finance Agent → `finance_records`
4. HITL approval → persistent `approval_records`
5. Audit layer → persistent `audit_records`
6. Dashboard → role-specific data-entry forms

# KOHLER Unified Enterprise AI Agent

> **Track 3 — Unified Enterprise AI Agent**
>
> A role-aware enterprise AI platform combining **RBAC, RAG, live synthetic enterprise data, multi-agent orchestration, Human-in-the-Loop (HITL) approvals, database actions, and audit logging**.

## 1. Project Overview

The KOHLER Unified Enterprise AI Agent is a prototype enterprise AI platform designed to let employees interact with company information and operational workflows through one AI dashboard.

The system is built around four principles:

1. **The right user sees the right information** through JWT authentication and role-based access control.
2. **Policies and documents are retrieved with RAG** rather than relying only on LLM generation.
3. **Live structured enterprise data is retrieved from databases** for employees, inventory, finance records, and operational state.
4. **Sensitive write operations require human approval** before the change is committed and audited.

The current prototype demonstrates authentication, RBAC, RAG, intent detection, multi-agent routing, HR/Finance/Operations agents, HITL approvals, action execution, audit logs, and a React dashboard.

### Final architecture extension

The final submission should include synthetic enterprise datasets and role-specific data-entry workflows:

- HR can submit new-joiner records.
- Operations can submit inventory/production changes.
- Finance can submit authorized financial changes.
- Submitted changes go through validation and approval.
- Approved changes are written to the live database.
- Subsequent queries read the updated state.

This creates a clear separation between **unstructured knowledge (RAG)** and **live structured enterprise state (SQL/database)**.

---

## 2. What Makes This Project Different

This is not only a chatbot over documents.

The differentiating architecture is:

**AI Assistant + RBAC + Multi-Agent Orchestration + RAG + Live Database Tools + HITL + Auditability**

The same natural-language interface can:

- answer policy questions from enterprise documents;
- query current structured data;
- route requests to the correct department agent;
- reject unauthorized requests before protected data is returned;
- create approval requests for sensitive changes;
- execute approved database mutations;
- record sensitive actions for auditing.

### Central design principle

> **RAG answers knowledge questions; database tools answer live-state questions; HITL protects sensitive state changes.**

---

## 3. Core Features

### Authentication
- Company-email login
- JWT access token
- Designation/role carried in the token
- Protected backend endpoints

### RBAC
Example roles:
- Employee
- Manager
- Finance Admin
- HR Admin
- Operations Manager
- Operations Admin
- GM

Permissions are enforced on the backend.

### Multi-Agent Orchestration
The orchestrator detects department and action type and routes requests to:
- HR Agent
- Finance / Enterprise Agent
- Operations Agent

### RAG
Knowledge-base documents include:
- `finance_policy.txt`
- `hr_policy.txt`
- `operations_data.txt`

RAG is intended for policies, procedures, manuals, and other unstructured knowledge.

### Live Enterprise Data
The final architecture uses synthetic SQL data for:
- employees
- departments
- inventory
- finance records
- operational records
- approved changes

### Human-in-the-Loop
Sensitive modifications follow:

`Request → Permission Check → Approval Request → GM Review → Execute → Audit`

Example:

`Change Hydraulic Pumps → GM approves → database is updated → audit log is written`

### Audit Logging
Records:
- requester
- action
- department/agent
- details
- approver
- status
- timestamp

### React Dashboard
Provides:
- login
- AI assistant
- role-aware dashboard
- pending approvals for GM
- audit logs for GM
- logout/session switching
- role-specific data-entry controls

---

## 4. System Architecture

```text
                         ┌──────────────────────┐
                         │      React UI        │
                         │ Login / Chat / Data  │
                         │ Entry / Approvals    │
                         └──────────┬───────────┘
                                    │ JWT
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │ Auth + RBAC + APIs   │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │    Orchestrator      │
                         │ Intent + Routing     │
                         └──────┬───────┬───────┘
                                │       │
                    ┌───────────┘       └───────────┐
                    ▼                               ▼
              HR / Finance /                 Operations Agent
              Enterprise Agent
                    │                               │
             ┌──────┴──────┐                 ┌──────┴──────┐
             ▼             ▼                 ▼             ▼
          RAG / KB      HR/Finance DB     RAG / KB    Operations DB
                    \       |                  /
                     \      |                 /
                      └──────┬───────────────┘
                             ▼
                       HITL Approval
                             │
                             ▼
                        Live Database
                             │
                             ▼
                         Audit Log
```

---

## 5. RAG vs Live Database

| Request | Source |
|---|---|
| How many paid leaves are allowed? | HR policy RAG |
| What is the finance modification policy? | Finance policy RAG |
| How many Finance employees are there? | Employee database |
| What is current inventory? | Operations database |
| What is current revenue? | Finance database |
| Add a new employee | HR database + approval workflow |
| Change inventory | Operations database + HITL |
| Who approved this change? | Audit database/log |

---

## 6. Repository Structure

```text
KOHLER/
├── backend/
│   ├── auth/
│   ├── agents/
│   ├── actions/
│   ├── audit/
│   ├── database/
│   ├── hitl/
│   ├── rag/
│   └── main.py
├── data/
│   └── documents/
├── frontend/
│   ├── src/
│   └── package.json
├── docs/
│   ├── KOHLER_Unified_Enterprise_AI_4_Page_Presentation.pdf
│   └── PROMPTS.md
├── .env.example
├── .gitignore
├── requirements.txt
├── PROMPTS.md
└── README.md
```

> Update the tree after the live database/data-entry modules are added so it exactly matches the final repository.

---

## 7. Technology Stack

**Backend:** Python, FastAPI, SQLAlchemy, SQLite, JWT

**AI/Retrieval:** LangChain, Ollama, Qwen2.5-Coder 3B, vector store/embeddings, RAG

**Frontend:** React, Vite, JavaScript, CSS

**Development:** VS Code / Antigravity IDE, Git, GitHub

**Local-first:** No paid software is required for the demonstrated local workflow.

---

## 8. Requirements

Install:
- Python 3.12
- Node.js + npm
- Git
- Ollama
- Qwen2.5-Coder 3B

```bash
ollama pull qwen2.5-coder:3b
```

---

## 9. Setup

### 1. Clone

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd KOHLER
```

### 2. Python environment

Windows:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Backend dependencies

```cmd
pip install -r requirements.txt
```

### 4. Environment

Create a local `.env`:

```env
SECRET_KEY=replace_with_a_local_secret
```

Do **not** commit `.env`. Commit `.env.example` instead.

### 5. Start Ollama

Make sure Ollama is running and the model is available.

### 6. Start backend

```cmd
python -m uvicorn backend.main:app --reload
```

Backend: `http://127.0.0.1:8000`

Swagger: `http://127.0.0.1:8000/docs`

### 7. Start frontend

```cmd
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

---

## 10. Synthetic Demo Accounts

| User | Email | Role |
|---|---|---|
| Rahul | `rahul@kohler.com` | Employee |
| Priya | `priya@kohler.com` | Manager |
| Arjun | `arjun@kohler.com` | Finance Admin |
| Mukund | `mukund@kohler.com` | GM |
| Operations Admin | `operations_admin@kohler.com` | Operations Admin |

These are synthetic demo identities.

---

## 11. Evaluation Demo

### Scenario 1 — Employee RBAC
Login as Rahul and ask:
- What is the current inventory?
- Show me the financial reports.
- Show me employee records.

Unauthorized requests should be denied.

### Scenario 2 — Manager
Login as Priya and ask:
- Show me my team information.
- What is the current inventory?

The system should apply manager-specific permissions.

### Scenario 3 — Finance HITL
Login as Arjun and submit a sensitive finance modification.

Login as Mukund (GM) → Pending Approvals → review → approve.

Verify execution and audit logging.

### Scenario 4 — Operations HITL + live data
Login as Operations Admin and submit an inventory change.

GM approves it.

Query the live inventory database again and verify the new value.

### Scenario 5 — GM
Demonstrate:
- cross-department visibility
- confidential authorization
- pending approvals
- audit logs
- current enterprise data

---

## 12. Role-Specific Data Entry

The final version supports controlled enterprise data entry.

Example — HR Admin adds a new joiner:

```text
HR Admin
   ↓
Add Employee Form
   ↓
Input Validation
   ↓
Permission Check
   ↓
Approval Request
   ↓
Authorized Approver
   ↓
Approved
   ↓
Employee Database
   ↓
Main Directory Updated
   ↓
Audit Log
```

The same pattern can be used for sensitive Finance and Operations changes.

---

## 13. Approach and Innovation

### Approach
The project treats an enterprise assistant as a combination of:
- identity
- permissions
- agents
- retrieval
- structured data tools
- controlled actions
- human oversight

### Innovation
The key design decision is the separation of **knowledge retrieval** from **live enterprise state**:

- RAG handles policies and documents.
- SQL/database tools handle current records.
- Agents select the appropriate source.
- HITL controls sensitive mutations.
- Audit logs provide traceability.

---

## 14. Technical Execution

The prototype demonstrates:
- JWT authentication
- backend-enforced RBAC
- permission-aware RAG
- intent detection
- multi-agent orchestration
- department-specific agents
- HITL approval creation
- GM approval
- action execution
- audit logging
- React frontend integration
- local LLM inference
- synthetic enterprise data architecture

---

## 15. User Experience and Feasibility

The system provides a single dashboard instead of requiring employees to understand backend systems.

Users can:
- ask natural-language questions;
- receive answers from the relevant agent;
- submit authorized changes;
- receive approval status;
- use role-specific dashboard controls.

The local-first prototype uses free/open tooling and synthetic data.

---

## 16. Business Sustainability and Impact

Potential enterprise value:
- faster access to departmental information;
- controlled enterprise actions;
- reduced accidental unauthorized access;
- traceable sensitive changes;
- a common AI interface across departments;
- a foundation for connecting HRIS, ERP, CRM, finance and inventory systems.

Synthetic data is used for safe demonstration without exposing real employee or financial information.

---

## 17. Security

Never commit:
- `.env`
- passwords
- API keys
- JWT secrets
- private credentials
- real employee personal information

Before submission:
- inspect staged files;
- verify no secrets are present;
- keep `.venv` and `node_modules` out of Git;
- enable GitHub secret scanning/push protection where available.

---

## 18. Demonstration Video

Recommended 4–6 minute sequence:

1. 0:00–0:30 — Problem and overview
2. 0:30–1:10 — Login + RBAC
3. 1:10–2:00 — RAG/policy query
4. 2:00–2:50 — Live enterprise data query
5. 2:50–3:50 — Sensitive modification + HITL
6. 3:50–4:30 — GM approval + database update
7. 4:30–5:00 — Audit log
8. 5:00–5:30 — Architecture + differentiator

---

## 19. Development Prompts

See [`PROMPTS.md`](PROMPTS.md).

The prompt record covers:
- Track 3 research
- enterprise architecture
- RBAC
- RAG
- multi-agent orchestration
- HITL
- audit logging
- frontend integration
- debugging
- live database architecture
- role-specific data entry

The prompt file is a reconstructed development record, not a verbatim export of the complete private conversation.

---

## 20. Submission Checklist

- [ ] Backend code uploaded
- [ ] Frontend code uploaded
- [ ] RAG documents uploaded
- [ ] Synthetic database/schema/seeding code uploaded
- [ ] Tests uploaded
- [ ] README uploaded
- [ ] PROMPTS.md uploaded
- [ ] 4-page PDF uploaded
- [ ] Demo video linked
- [ ] `.env.example` uploaded
- [ ] `.env` excluded
- [ ] `.venv` excluded
- [ ] `node_modules` excluded
- [ ] No passwords/API keys/tokens
- [ ] Repository can be cloned and started from README
- [ ] Live-data workflow tested
- [ ] Data-entry/approval workflow tested
- [ ] GitHub URL copied into the submission email

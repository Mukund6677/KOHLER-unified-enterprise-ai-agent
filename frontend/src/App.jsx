import { useState } from "react";
import "./App.css";

function App() {
  const [approvals, setApprovals] = useState([]);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loggedIn, setLoggedIn] = useState(
    !!localStorage.getItem("token")
  );

  const [employee, setEmployee] = useState(
    localStorage.getItem("employee") || ""
  );

  const [designation, setDesignation] = useState(
    localStorage.getItem("designation") || ""
  );

  const [page, setPage] = useState("dashboard");
  const [showAuditLogs, setShowAuditLogs] = useState(false);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  // =========================
  // FETCH PENDING APPROVALS
  // =========================

  const fetchApprovals = async () => {
    console.log("Fetching approvals...");

    const token = localStorage.getItem("token");

    try {
      const res = await fetch(
        "http://127.0.0.1:8000/approval/pending",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await res.json();

      console.log("Approval response:", data);

      if (res.ok) {
        setApprovals(data.approvals || []);
      } else {
        console.error("Approval request failed:", data);
        alert(data.detail || "Unable to fetch approvals.");
      }

    } catch (error) {
      console.error("Approval connection error:", error);
      alert("Unable to connect to KOHLER AI service.");
    }
  };


  // =========================
  // APPROVE REQUEST
  // =========================

  const approveRequest = async (requestId) => {
  const token = localStorage.getItem("token");

  try {
    const res = await fetch(
      `http://127.0.0.1:8000/approval/approve?request_id=${requestId}`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await res.json();

    console.log("Approval result:", data);

    if (res.ok) {
      console.log("Approval successful:", data);
      alert("Approval successful!");
      await fetchApprovals();
    } else {
      console.error("Approval failed:", data);
      alert(data.detail || "Approval failed.");
    }

  } catch (error) {
    console.error("Approval error:", error);
    alert("Unable to connect to KOHLER AI service.");
  }
};

  // =========================
// AUDIT LOGS
// =========================

const fetchAuditLogs = async () => {
  const token = localStorage.getItem("token");

  try {
    const res = await fetch(
      "http://127.0.0.1:8000/audit/logs",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await res.json();

    if (res.ok) {
      setAuditLogs(data.logs || []);
      setShowAuditLogs(true);
    } else {
      alert(data.detail || "Unable to fetch audit logs.");
    }

  } catch (error) {
    console.error("Audit log error:", error);
    alert("Unable to connect to KOHLER AI service.");
  }
};

  /* =========================
     LOGIN
  ========================= */

  const login = async () => {
    const cleanEmail = email.trim().toLowerCase();

    if (!cleanEmail || !password) {
      alert("Please enter your company email and password.");
      return;
    }

    console.log("LOGIN EMAIL:", cleanEmail);

    try {
      const res = await fetch(
        "http://127.0.0.1:8000/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: cleanEmail,
            password: password,
          }),
        }
      );

      const data = await res.json();

      console.log("LOGIN RESPONSE:", res.status, data);

      if (!res.ok) {
        localStorage.removeItem("token");
        localStorage.removeItem("employee");
        localStorage.removeItem("designation");

        alert(data.detail || "Login failed");
        return;
      }

      localStorage.setItem("token", data.access_token);
      localStorage.setItem("employee", data.employee);
      localStorage.setItem("designation", data.designation);

      setEmployee(data.employee);
      setDesignation(data.designation);
      setLoggedIn(true);
      setPage("dashboard");

      setPassword("");

    } catch (error) {
      console.error("LOGIN ERROR:", error);
      alert("Unable to connect to KOHLER AI backend.");
    }
  };
  /* =========================
     LOGOUT
  ========================= */

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("employee");
    localStorage.removeItem("designation");

    setLoggedIn(false);
    setEmployee("");
    setDesignation("");
    setEmail("");
    setPassword("");
    setPage("dashboard");
    setMessages([]);
  };

  /* =========================
     AI ASSISTANT
  ========================= */

  const sendQuery = async () => {
    if (!query.trim()) return;

    const userMessage = {
      role: "user",
      text: query,
    };

    setMessages((previous) => [...previous, userMessage]);

    const currentQuery = query;
    setQuery("");

    try {
      /*
       * We will connect this to the existing
       * secure RAG endpoint.
       */

      const token = localStorage.getItem("token");

      const res = await fetch(
  `http://127.0.0.1:8000/secure-search?query=${encodeURIComponent(
    currentQuery
  )}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await res.json();

      if (!res.ok) {
        setMessages((previous) => [
          ...previous,
          {
            role: "assistant",
            text:
              data.detail ||
              "You do not have permission to access this information.",
          },
        ]);

        return;
      }

      let answer = "";

      if (data.result?.answer) {
        answer = `🤖 ${data.agent}\n\n${data.result.answer}`;

      } else if (data.result?.message) {
        answer = `🤖 ${data.agent}\n\n${data.result.message}`;

      } else if (data.answer) {
        answer = data.answer;

      } else if (data.message) {
        answer = data.message;

      } else if (data.results) {
        answer = data.results.join("\n\n");

      } else {
        answer = JSON.stringify(data);
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: answer,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text:
            "Unable to connect to the KOHLER AI service.",
        },
      ]);
    }
  };

  /* =========================
     LOGIN SCREEN
  ========================= */

  if (!loggedIn) {
    return (
      <div className="login-page">
        <div className="login-card">

          <h1>KOHLER</h1>

          <p className="login-subtitle">
            Unified Enterprise AI Agent
          </p>

          <input
            type="email"
            placeholder="Enter company email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                login();
              }
            }}
          />

          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                login();
              }
            }}
          />

          <button onClick={login}>
            Login
          </button>

          <div className="login-info">
            <span>Secure enterprise access</span>
            <span>Role-based permissions</span>
          </div>

        </div>
      </div>
    );
  }

  /* =========================
     MAIN APPLICATION
  ========================= */

  return (
    <div className="dashboard">

      {/* =========================
          SIDEBAR
      ========================= */}

      <aside className="sidebar">

        <div className="sidebar-logo">
          KOHLER
        </div>

        <div className="sidebar-subtitle">
          Enterprise AI
        </div>

        <nav>

          <div
            className={`nav-item ${
              page === "dashboard" ? "active" : ""
            }`}
            onClick={() => setPage("dashboard")}
          >
            Dashboard
          </div>

          <div
            className={`nav-item ${
              page === "assistant" ? "active" : ""
            }`}
            onClick={() => setPage("assistant")}
          >
            AI Assistant
          </div>

          <div
            className="nav-item"
            onClick={() => setPage("knowledge")}
          >
            Knowledge Base
          </div>

          {designation === "Finance Admin" && (
            <div
              className="nav-item"
              onClick={() => setPage("finance")}
            >
              Finance
            </div>
          )}

          {designation === "GM" && (
            <div
              className="nav-item"
              onClick={() => setPage("confidential")}
            >
              Confidential Data
            </div>
          )}

          {(designation === "Manager" ||
            designation === "GM") && (
            <div
              className="nav-item"
              onClick={() => setPage("team")}
            >
              Team Insights
            </div>
          )}

          {(designation === "Operations Admin" ||
            designation === "Operations Manager" ||
            designation === "GM") && (

            <div
              className={`nav-item ${
                page === "operations" ? "active" : ""
              }`}
              onClick={() => setPage("operations")}
            >
              Operations
            </div>

          )}

        </nav>

        <button
          className="logout-button"
          onClick={logout}
        >
          Logout
        </button>

      </aside>

      {/* =========================
          MAIN CONTENT
      ========================= */}

      <main className="main-content">

        {/* HEADER */}

        <header className="dashboard-header">

          <div>
            <h2>
              {page === "assistant"
                ? "AI Assistant"
                : page === "dashboard"
                ? `Welcome, ${employee}`
                : "KOHLER Enterprise AI"}
            </h2>

            <p>
              KOHLER Unified Enterprise AI Agent
            </p>
          </div>

          <div className="user-badge">

            <div className="avatar">
              {employee.charAt(0)}
            </div>

            <div>
              <strong>{employee}</strong>
              <span>{designation}</span>
            </div>

          </div>

        </header>


        {/* =========================
            AI ASSISTANT PAGE
        ========================= */}

        {page === "assistant" && (

          <section className="assistant-page">

            <div className="assistant-header">

              <div>
                <span className="small-label">
                  ROLE-AWARE ENTERPRISE AI
                </span>

                <h2>
                  Ask KOHLER AI
                </h2>

                <p>
                  Your responses are generated using
                  information available to your role.
                </p>
              </div>

              <div className="assistant-role">
                {designation}
              </div>

            </div>


            <div className="chat-container">

              <div className="chat-messages">

                {messages.length === 0 && (

                  <div className="empty-chat">

                    <div className="empty-icon">
                      AI
                    </div>

                    <h3>
                      How can I help you?
                    </h3>

                    <p>
                      Ask a question about enterprise
                      information available to you.
                    </p>

                    <div className="example-questions">

                      <button
                        onClick={() =>
                          setQuery(
                            "What financial information can I access?"
                          )
                        }
                      >
                        What financial information can I access?
                      </button>

                      <button
                        onClick={() =>
                          setQuery(
                            "What are my permissions?"
                          )
                        }
                      >
                        What are my permissions?
                      </button>

                      <button
                        onClick={() =>
                          setQuery(
                            "What information is available to my role?"
                          )
                        }
                      >
                        What information is available to my role?
                      </button>

                    </div>

                  </div>

                )}


                {messages.map((message, index) => (

                  <div
                    key={index}
                    className={`chat-message ${
                      message.role === "user"
                        ? "user-message"
                        : "ai-message"
                    }`}
                  >

                    <div className="message-label">
                      {message.role === "user"
                        ? employee
                        : "KOHLER AI"}
                    </div>

                    <div className="message-text">
                      {message.text}
                    </div>

                  </div>

                ))}

              </div>


              <div className="chat-input-area">

                <input
                  type="text"
                  placeholder="Ask KOHLER AI..."
                  value={query}
                  onChange={(e) =>
                    setQuery(e.target.value)
                  }
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      sendQuery();
                    }
                  }}
                />

                <button onClick={sendQuery}>
                  Send →
                </button>

              </div>

            </div>

          </section>

        )}

        {/* OPERATIONS PAGE */}

        {page === "operations" && (

          <section className="assistant-page">

            <div className="assistant-header">
              <div>
                <span className="small-label">
                  OPERATIONS CONTROL
                </span>

                <h2>
                  Operations Management
                </h2>

                <p>
                  View operational information and manage
                  sensitive operational changes.
                </p>
              </div>

              <div className="assistant-role">
                {designation}
              </div>
            </div>

            <div className="dashboard-grid">

              <div className="dashboard-card">
                <div className="card-icon">
                  OP
                </div>

                <h3>
                  Production & Inventory
                </h3>

                <p>
                  Ask KOHLER AI about production,
                  inventory, suppliers and plant operations.
                </p>

                <button
                  className="card-button"
                  onClick={() => setPage("assistant")}
                >
                  Ask AI →
                </button>
              </div>

              <div className="dashboard-card highlight">
                <div className="card-icon">
                  HITL
                </div>

                <h3>
                  Sensitive Changes
                </h3>

                <p>
                  Operational changes require General
                  Manager approval before execution.
                </p>

                <button
                  className="card-button"
                  onClick={() => setPage("assistant")}
                >
                  Request Change →
                </button>
              </div>

            </div>

          </section>

        )}

        {/* =========================
            DASHBOARD
        ========================= */}

        {page === "dashboard" && (

          <>

            <section className="role-banner">

              <div>

                <span className="small-label">
                  CURRENT ACCESS LEVEL
                </span>

                <h3>
                  {designation}
                </h3>

                <p>
                  Your AI capabilities and knowledge
                  access are controlled by your
                  organizational role.
                </p>

              </div>

              <div className="security-status">

                <span className="status-dot"></span>

                Access Controlled

              </div>

            </section>


            <section className="dashboard-grid">

              {/* AI ASSISTANT */}

              <div className="dashboard-card">

                <div className="card-icon">
                  AI
                </div>

                <h3>
                  AI Assistant
                </h3>

                <p>
                  Ask the enterprise AI agent questions
                  using information available to your role.
                </p>

                <button
                  className="card-button"
                  onClick={() => setPage("assistant")}
                >
                  Open Assistant →
                </button>

              </div>


              {/* KNOWLEDGE BASE */}

              <div className="dashboard-card">

                <div className="card-icon">
                  KB
                </div>

                <h3>
                  Knowledge Base
                </h3>

                <p>
                  Search enterprise documents and retrieve
                  information according to your permissions.
                </p>

                <button
                  className="card-button"
                  onClick={() => setPage("knowledge")}
                >
                  Search Knowledge →
                </button>

              </div>


              {/* ACCESS CONTROL */}

              <div className="dashboard-card">

                <div className="card-icon">
                  AC
                </div>

                <h3>
                  Access Control
                </h3>

                <p>
                  Your current role determines which
                  enterprise resources you can access.
                </p>

                <button
                  className="card-button"
                  onClick={() => setPage("permissions")}
                >
                  View Permissions →
                </button>

              </div>


              {/* FINANCE ADMIN */}

              {designation === "Finance Admin" && (

                <div className="dashboard-card highlight">

                  <div className="card-icon">
                    FN
                  </div>

                  <h3>
                    Finance Operations
                  </h3>

                  <p>
                    Access finance records and submit
                    sensitive changes for approval through HITL.
                  </p>

                  <button
                    className="card-button"
                    onClick={() => setPage("finance")}
                  >
                    Open Finance →
                  </button>

                </div>

              )}


              {/* MANAGER */}

              {designation === "Manager" && (



                <div className="dashboard-card highlight">

                  <div className="card-icon">
                    TM
                  </div>

                  <h3>
                    Team Insights
                  </h3>

                  <p>
                    Access information relevant to your
                    team and management responsibilities.
                  </p>

                  <button
                    className="card-button"
                    onClick={() => setPage("team")}
                  >
                    View Team →
                  </button>

                </div>

              )}

              {/* OPERATIONS ADMIN */}

              {designation === "Operations Admin" && (

                <div className="dashboard-card highlight">

                  <div className="card-icon">
                    OP
                  </div>

                  <h3>
                    Operations Control
                  </h3>

                  <p>
                    Access production and inventory information
                    and submit sensitive operational changes for
                    General Manager approval.
                  </p>

                  <button
                    className="card-button"
                    onClick={() => setPage("operations")}
                  >
                    Open Operations →
                  </button>

                </div>

              )}

              {/* GM */}

              {designation === "GM" && (

              <>
                <div className="dashboard-card confidential">

                  <div className="card-icon">
                    GM
                  </div>

                  <h3>
                    Executive Intelligence
                  </h3>

                  <p>
                    Access confidential company-level
                    information permitted for General Management.
                  </p>

                  <button
                    className="card-button"
                    onClick={() => setPage("confidential")}
                  >
                    Open Executive View →
                  </button>

                </div>

                {designation === "GM" && (
                  <>
                    {/* Pending Approvals */}

                    <div className="dashboard-card">

                      <div className="card-icon">
                        ✓
                      </div>

                      <h3>
                        Pending Approvals
                      </h3>

                      <p>
                        Review and approve sensitive actions
                        submitted by employees.
                      </p>

                      <button
                        type="button"
                        className="card-button"
                        onClick={() => {
                          alert("Fetching approvals...");
                          fetchApprovals();
                        }}
                      >
                        View Pending Requests →
                      </button>

                      {approvals.length > 0 && (
                        <div className="approval-list">

                          {approvals.map((approval) => (

                            <div
                              key={approval.id}
                              className="approval-item"
                            >

                              <p>
                                <strong>Action:</strong>{" "}
                                {approval.action}
                              </p>

                              <p>
                                <strong>Request:</strong>{" "}
                                {approval.details}
                              </p>

                              <p>
                                <strong>Status:</strong>{" "}
                                {approval.status}
                              </p>

                              <button
                                className="card-button"
                                onClick={() =>
                                  approveRequest(approval.id)
                                }
                              >
                                Approve
                              </button>

                            </div>

                          ))}

                        </div>
                      )}

                    </div>
                  </>
                )}

                {/* Audit Logs */}

                <div className="dashboard-card">

                  <div className="card-icon">
                    AL
                  </div>

                  <h3>
                    Audit Logs
                  </h3>

                  <p>
                    Review a secure record of sensitive actions,
                    approvals, and administrative activity.
                  </p>

                  <button
                    type="button"
                    className="card-button"
                    onClick={fetchAuditLogs}
                  >
                    View Audit Logs →
                  </button>

                  {showAuditLogs && auditLogs.length > 0 && (
                    <div className="approval-list">

                      {auditLogs.map((log, index) => (

                        <div
                          key={index}
                          className="approval-item"
                        >

                          <p>
                            <strong>Action:</strong>{" "}
                            {log.action}
                          </p>

                          <p>
                            <strong>Employee:</strong>{" "}
                            {log.employee}
                          </p>

                          <p>
                            <strong>Approved By:</strong>{" "}
                            {log.approved_by}
                          </p>

                          <p>
                            <strong>Status:</strong>{" "}
                            {log.status}
                          </p>

                          <p>
                            <strong>Time:</strong>{" "}
                            {log.timestamp}
                          </p>

                          <p>
                            <strong>Details:</strong>{" "}
                            {log.details}
                          </p>

                        </div>

                      ))}

                    </div>
                  )}

                </div>

              </>

            )}

            </section>


            <section className="security-panel">

              <h3>
                Enterprise Security
              </h3>

              <div className="security-grid">

                <div>
                  <strong>
                    ✓ Identity Verified
                  </strong>

                  <span>
                    Authenticated employee
                  </span>
                </div>

                <div>
                  <strong>
                    ✓ Role Verified
                  </strong>

                  <span>
                    {designation} permissions applied
                  </span>
                </div>

                <div>
                  <strong>
                    ✓ RAG Access Control
                  </strong>

                  <span>
                    Knowledge filtered by role
                  </span>
                </div>

                <div>
                  <strong>
                    ✓ HITL Enabled
                  </strong>

                  <span>
                    Sensitive actions require approval
                  </span>
                </div>

              </div>

            </section>

          </>
        )}

      </main>
    </div>
  );
}

export default App;
import { useState } from "react";

export default function Index() {
  const [isSignedIn, setIsSignedIn] = useState(false);

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: 16,
        background:
          "linear-gradient(135deg, rgb(15,23,42), rgb(30,41,59), rgb(15,23,42))",
        color: "#e2e8f0",
        fontFamily:
          'ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji"',
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: 560,
          borderRadius: 16,
          border: "1px solid rgb(51,65,85)",
          background: "rgba(30,41,59,0.55)",
          backdropFilter: "blur(10px)",
          padding: 24,
        }}
      >
        <div style={{ textAlign: "center", marginBottom: 18 }}>
          <div
            style={{
              margin: "0 auto 14px",
              height: 80,
              width: 80,
              borderRadius: "999px",
              background: "rgba(59,130,246,0.12)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 34,
            }}
            aria-hidden="true"
          >
            🛡️
          </div>

          <h1 style={{ fontSize: 30, fontWeight: 800, margin: 0 }}>
            SecureWorks
          </h1>
          <p style={{ marginTop: 8, color: "#94a3b8" }}>
            Enterprise Security Monitoring Demo
          </p>
        </div>

        <p style={{ textAlign: "center", color: "#cbd5e1", marginBottom: 18 }}>
          Welcome to the SecureWorks Demo App — a simulated internal company login
          portal that generates realistic security event logs for monitoring.
        </p>

        <div style={{ marginBottom: 18 }}>
          <h3 style={{ fontSize: 13, fontWeight: 700, marginBottom: 10 }}>
            Demo Credentials:
          </h3>

          <div
            style={{
              borderRadius: 12,
              border: "1px solid rgb(71,85,105)",
              background: "rgba(51,65,85,0.35)",
              padding: 14,
              display: "grid",
              gap: 10,
              fontSize: 13,
            }}
          >
            <Row label="Standard User:" value="user@secureworks.demo" />
            <Row label="Admin User:" value="admin@secureworks.demo" />
            <Row
              label="Passwords:"
              value="Password123! / AdminPassword123!"
            />
          </div>
        </div>

        <button
          onClick={() => setIsSignedIn((v) => !v)}
          style={{
            width: "100%",
            padding: "12px 14px",
            borderRadius: 12,
            border: "1px solid rgb(59,130,246)",
            background: "rgb(59,130,246)",
            color: "white",
            fontWeight: 700,
            cursor: "pointer",
          }}
        >
          {isSignedIn ? "Go to Dashboard →" : "Sign In →"}
        </button>

        <p style={{ marginTop: 12, fontSize: 12, color: "#94a3b8" }}>
          (UI-only for Phase 0/1. Auth + routing will come later.)
        </p>
      </div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        gap: 12,
        alignItems: "center",
      }}
    >
      <span style={{ color: "#94a3b8" }}>{label}</span>
      <code style={{ color: "#e2e8f0" }}>{value}</code>
    </div>
  );
}

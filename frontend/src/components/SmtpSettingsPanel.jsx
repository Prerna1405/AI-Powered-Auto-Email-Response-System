import { useEffect, useState } from "react";
import { Send, CheckCircle, XCircle, Loader } from "lucide-react";
import toast from "react-hot-toast";
import axios from "../lib/axios";

export default function SmtpSettingsPanel() {
  const [status, setStatus] = useState(null);
  const [form, setForm] = useState({
    smtp_host: "smtp.gmail.com",
    smtp_port: 465,
    smtp_user: "",
    smtp_password: "",
    delivery_mode: "smtp",
  });
  const [testEmail, setTestEmail] = useState("");
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);

  useEffect(() => {
    axios.get("/api/email-delivery/status").then((r) => {
      setStatus(r.data);
      if (r.data.smtp_config) {
        setForm((prev) => ({ ...prev, ...r.data.smtp_config }));
      }
    });
  }, []);

  const save = async () => {
    try {
      await axios.post("/api/email-delivery/configure-smtp", form);
      toast.success("Saved. Restart backend and worker to apply.");
      const r = await axios.get("/api/email-delivery/status");
      setStatus(r.data);
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Save failed");
    }
  };

  const sendTest = async () => {
    if (!testEmail) return toast.error("Enter your email address");
    setTesting(true);
    setTestResult(null);
    try {
      const r = await axios.post("/api/email-delivery/test", { to_email: testEmail });
      setTestResult(r.data);
    } catch (e) {
      setTestResult({
        success: false,
        error: e?.response?.data?.detail || "Request failed",
      });
    } finally {
      setTesting(false);
    }
  };

  return (
    <div id="email-delivery" className="max-w-2xl mt-8">
      <h3 className="font-semibold text-lg mb-3">Email Delivery (SMTP)</h3>
      <p className="text-sm text-slate-600 mb-3">
        Configure SMTP to send real auto-replies to customer inboxes.
      </p>
      {status && (
        <p className="text-xs mb-4">
          Active mode: <strong>{status.active_method}</strong> | Real delivery:{" "}
          <strong>{status.real_delivery_active ? "ON" : "OFF"}</strong>
        </p>
      )}

      <div className="grid grid-cols-2 gap-3">
        <input
          className="border rounded p-2"
          value={form.smtp_host}
          onChange={(e) => setForm((p) => ({ ...p, smtp_host: e.target.value }))}
          placeholder="SMTP host"
        />
        <input
          type="number"
          className="border rounded p-2"
          value={form.smtp_port}
          onChange={(e) => setForm((p) => ({ ...p, smtp_port: Number(e.target.value) }))}
          placeholder="SMTP port"
        />
        <input
          className="border rounded p-2"
          value={form.smtp_user}
          onChange={(e) => setForm((p) => ({ ...p, smtp_user: e.target.value }))}
          placeholder="SMTP user"
        />
        <input
          type="password"
          className="border rounded p-2"
          value={form.smtp_password}
          onChange={(e) => setForm((p) => ({ ...p, smtp_password: e.target.value }))}
          placeholder="SMTP password / app password"
        />
      </div>
      <button className="mt-3 bg-cyan-700 text-white px-4 py-2 rounded" onClick={save}>
        Save SMTP Settings
      </button>

      <div className="mt-6 border rounded p-4 bg-slate-50">
        <h4 className="font-semibold mb-2">Send Test Email</h4>
        <div className="flex gap-2">
          <input
            className="border rounded p-2 flex-1"
            value={testEmail}
            onChange={(e) => setTestEmail(e.target.value)}
            placeholder="your@email.com"
          />
          <button
            onClick={sendTest}
            disabled={testing}
            className="bg-emerald-700 text-white px-4 py-2 rounded flex items-center gap-2"
          >
            {testing ? <Loader size={14} className="animate-spin" /> : <Send size={14} />}
            {testing ? "Sending..." : "Send Test"}
          </button>
        </div>
        {testResult && (
          <div
            className={`mt-3 p-3 rounded border ${
              testResult.success
                ? "bg-green-50 border-green-300 text-green-700"
                : "bg-red-50 border-red-300 text-red-700"
            }`}
          >
            <div className="flex items-start gap-2">
              {testResult.success ? <CheckCircle size={16} /> : <XCircle size={16} />}
              <div>
                {testResult.success ? (
                  <span>Email delivered. Check inbox at {testEmail}</span>
                ) : (
                  <span>
                    Failed: {testResult.error}
                    {testResult.fix ? ` | Fix: ${testResult.fix}` : ""}
                  </span>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

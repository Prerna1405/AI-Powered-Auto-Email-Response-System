import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function InboxPage() {
  const [emails, setEmails] = useState([]);
  const [folder, setFolder] = useState("all");
  const [selected, setSelected] = useState(null);
  const [detail, setDetail] = useState(null);
  const [form, setForm] = useState({
    from_email: "john@example.com",
    from_name: "John",
    subject: "I forgot my password",
    body: "Hi, I cannot log in. Please help with password reset.",
    transport_mode: "simulator",
  });

  const load = () => api.get(`/emails?folder=${folder}`).then((r) => setEmails(r.data));
  useEffect(() => {
    load();
    const id = setInterval(load, 4000);
    return () => clearInterval(id);
  }, [folder]);

  useEffect(() => {
    if (!selected) return;
    api.get(`/emails/${selected}`).then((r) => setDetail(r.data));
  }, [selected, emails]);

  const send = async () => {
    await api.post("/emails/simulate-send", form);
    load();
  };

  return (
    <div className="grid grid-cols-4 gap-4">
      <div className="col-span-1 bg-white p-4 rounded shadow">
        <h2 className="font-semibold mb-3">Compose (Simulator)</h2>
        {["from_email", "from_name", "subject"].map((k) => (
          <input
            key={k}
            className="w-full border rounded p-2 mb-2"
            value={form[k]}
            onChange={(e) => setForm({ ...form, [k]: e.target.value })}
            placeholder={k}
          />
        ))}
        <textarea
          className="w-full border rounded p-2 mb-2 h-28"
          value={form.body}
          onChange={(e) => setForm({ ...form, body: e.target.value })}
        />
        <button className="bg-slate-900 text-white px-4 py-2 rounded" onClick={send}>
          Send
        </button>
      </div>
      <div className="col-span-2 bg-white p-4 rounded shadow">
        <h2 className="font-semibold mb-3">Gmail-Style Folders</h2>
        <div className="flex gap-2 mb-3">
          {["all", "inbox", "sent", "escalated", "failed"].map((f) => (
            <button
              key={f}
              className={`px-3 py-1 rounded text-sm ${folder === f ? "bg-slate-900 text-white" : "bg-slate-100"}`}
              onClick={() => setFolder(f)}
            >
              {f}
            </button>
          ))}
        </div>
        <div className="space-y-2">
          {emails.map((e) => (
            <button key={e.id} className="border rounded p-3 text-left w-full" onClick={() => setSelected(e.id)}>
              <p className="font-semibold">{e.subject}</p>
              <p className="text-sm text-slate-600">{e.from_name} ({e.from_email})</p>
              <p className="text-sm">{e.body.slice(0, 120)}</p>
              <span className="text-xs bg-slate-100 px-2 py-1 rounded">{e.status}</span>
            </button>
          ))}
        </div>
      </div>
      <div className="col-span-1 bg-white p-4 rounded shadow">
        <h2 className="font-semibold mb-3">AI Analysis + Reply</h2>
        {!detail && <p className="text-sm text-slate-500">Select an email to view details.</p>}
        {detail && (
          <div className="space-y-3 text-sm">
            <pre className="bg-slate-100 p-2 rounded overflow-auto text-xs">
              {JSON.stringify(detail.email?.ai_analysis || {}, null, 2)}
            </pre>
            <div>
              <p className="font-semibold">Auto Reply</p>
              <div
                className="border rounded p-2 max-h-64 overflow-auto"
                dangerouslySetInnerHTML={{ __html: detail.reply?.generated_reply || "<i>No reply sent yet.</i>" }}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

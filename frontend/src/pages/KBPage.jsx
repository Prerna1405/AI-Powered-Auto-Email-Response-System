import { useEffect, useState } from "react";
import { api } from "../api/client";

const empty = {
  category: "Account Issues",
  intent: "",
  keywords: [],
  problem_summary: "",
  solution_template: "",
  variables_used: [],
  confidence_threshold: 75,
};

export default function KBPage() {
  const [rows, setRows] = useState([]);
  const [form, setForm] = useState(empty);
  const load = () => api.get("/kb").then((r) => setRows(r.data));
  useEffect(() => void load(), []);

  const create = async () => {
    await api.post("/kb", { ...form, keywords: form.keywords, variables_used: form.variables_used });
    setForm(empty);
    load();
  };

  return (
    <div className="space-y-4">
      <div className="bg-white rounded shadow p-4">
        <h2 className="font-semibold mb-2">Add KB Article</h2>
        <input className="border p-2 rounded w-full mb-2" placeholder="Intent" value={form.intent}
          onChange={(e) => setForm({ ...form, intent: e.target.value })} />
        <textarea className="border p-2 rounded w-full mb-2" placeholder="Problem summary" value={form.problem_summary}
          onChange={(e) => setForm({ ...form, problem_summary: e.target.value })} />
        <textarea className="border p-2 rounded w-full mb-2" placeholder="Solution template" value={form.solution_template}
          onChange={(e) => setForm({ ...form, solution_template: e.target.value })} />
        <button className="bg-slate-900 text-white px-4 py-2 rounded" onClick={create}>Create</button>
      </div>
      <div className="bg-white rounded shadow p-4">
        <h2 className="font-semibold mb-2">Knowledge Base ({rows.length})</h2>
        {rows.map((r) => <div key={r.id} className="border-b py-2">{r.intent} - {r.category}</div>)}
      </div>
    </div>
  );
}

import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function PreviewPage() {
  const [selected, setSelected] = useState(null);
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    api.get("/emails").then((r) => {
      setEmails(r.data);
      if (r.data.length) setSelected(r.data[0].id);
    });
  }, []);

  const current = emails.find((e) => e.id === selected);

  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="bg-white rounded shadow p-4">
        <h2 className="font-semibold">Original Email</h2>
        <select className="border rounded p-2 w-full my-2" onChange={(e) => setSelected(e.target.value)}>
          {emails.map((e) => <option key={e.id} value={e.id}>{e.subject}</option>)}
        </select>
        {current && (
          <div>
            <p><strong>From:</strong> {current.from_email}</p>
            <p><strong>Subject:</strong> {current.subject}</p>
            <p>{current.body}</p>
          </div>
        )}
      </div>
      <div className="bg-white rounded shadow p-4">
        <h2 className="font-semibold">AI Analysis</h2>
        <pre className="bg-slate-100 p-3 rounded text-xs overflow-auto">
          {JSON.stringify(current?.ai_analysis || {}, null, 2)}
        </pre>
      </div>
    </div>
  );
}

import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function DashboardPage() {
  const [data, setData] = useState({ total: 0, auto_resolved_pct: 0, escalated_pct: 0, failed: 0 });

  useEffect(() => {
    api.get("/analytics/overview").then((res) => setData(res.data));
  }, []);

  return (
    <div className="grid grid-cols-2 gap-4">
      <Card title="Emails Received" value={data.total} />
      <Card title="Auto-Resolved %" value={data.auto_resolved_pct.toFixed(1)} />
      <Card title="Escalated %" value={data.escalated_pct.toFixed(1)} />
      <Card title="Failed" value={data.failed} />
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div className="bg-white rounded shadow p-4">
      <p className="text-slate-500">{title}</p>
      <p className="text-3xl font-semibold">{value}</p>
    </div>
  );
}

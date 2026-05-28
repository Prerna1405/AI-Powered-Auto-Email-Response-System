import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function AnalyticsPage() {
  const [categories, setCategories] = useState({});
  const [coverage, setCoverage] = useState({ coverage_pct: 0 });

  useEffect(() => {
    api.get("/analytics/categories").then((r) => setCategories(r.data));
    api.get("/analytics/kb-coverage").then((r) => setCoverage(r.data));
  }, []);

  return (
    <div className="space-y-4">
      <div className="bg-white p-4 rounded shadow">
        <h2 className="font-semibold">Category Distribution</h2>
        {Object.entries(categories).map(([k, v]) => (
          <div key={k} className="flex justify-between border-b py-1">
            <span>{k}</span><span>{v}</span>
          </div>
        ))}
      </div>
      <div className="bg-white p-4 rounded shadow">
        <h2 className="font-semibold">KB Coverage</h2>
        <p className="text-2xl">{coverage.coverage_pct.toFixed(1)}%</p>
      </div>
    </div>
  );
}

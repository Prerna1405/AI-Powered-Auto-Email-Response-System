import { useEffect, useState } from "react";
import { api } from "../api/client";
import SmtpSettingsPanel from "../components/SmtpSettingsPanel";

export default function SettingsPage() {
  const [settings, setSettings] = useState(null);

  useEffect(() => {
    api.get("/settings").then((r) => setSettings(r.data));
  }, []);

  if (!settings) return <div>Loading...</div>;

  const save = async () => {
    await api.put("/settings", settings);
    alert("Saved");
  };

  return (
    <div className="bg-white rounded shadow p-4 max-w-2xl space-y-2">
      <h2 className="font-semibold">System Settings</h2>
      <input className="border p-2 rounded w-full" value={settings.company_name}
        onChange={(e) => setSettings({ ...settings, company_name: e.target.value })} />
      <input className="border p-2 rounded w-full" value={settings.support_email}
        onChange={(e) => setSettings({ ...settings, support_email: e.target.value })} />
      <label className="flex items-center gap-2">
        <input type="checkbox" checked={settings.gmail_connected}
          onChange={(e) => setSettings({ ...settings, gmail_connected: e.target.checked })} />
        Gmail Connected
      </label>
      <label className="flex items-center gap-2">
        <input type="checkbox" checked={settings.auto_reply_enabled}
          onChange={(e) => setSettings({ ...settings, auto_reply_enabled: e.target.checked })} />
        Auto Reply Enabled
      </label>
      <button className="bg-slate-900 text-white px-4 py-2 rounded" onClick={save}>Save</button>
      <SmtpSettingsPanel />
    </div>
  );
}

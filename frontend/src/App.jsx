import { NavLink, Route, Routes } from "react-router-dom";
import { motion } from "framer-motion";
import { Toaster } from "react-hot-toast";
import DashboardPage from "./pages/DashboardPage";
import InboxPage from "./pages/InboxPage";
import KBPage from "./pages/KBPage";
import PreviewPage from "./pages/PreviewPage";
import AnalyticsPage from "./pages/AnalyticsPage";
import SettingsPage from "./pages/SettingsPage";
import DeliveryModeBanner from "./components/DeliveryModeBanner";

const nav = [
  ["Dashboard", "/"],
  ["Inbox", "/inbox"],
  ["Knowledge Base", "/kb"],
  ["Reply Preview", "/preview"],
  ["Analytics", "/analytics"],
  ["Settings", "/settings"],
];

export default function App() {
  return (
    <div className="min-h-screen bg-slate-100">
      <Toaster position="top-right" />
      <DeliveryModeBanner />
      <header className="bg-slate-900 text-white p-4">
        <h1 className="text-xl font-semibold">AI-Powered Automatic Email Response System</h1>
      </header>
      <div className="flex">
        <aside className="w-64 bg-white border-r min-h-screen p-4 space-y-2">
          {nav.map(([label, to]) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `block rounded px-3 py-2 ${isActive ? "bg-slate-900 text-white" : "hover:bg-slate-100"}`
              }
            >
              {label}
            </NavLink>
          ))}
        </aside>
        <main className="flex-1 p-6">
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/inbox" element={<InboxPage />} />
              <Route path="/kb" element={<KBPage />} />
              <Route path="/preview" element={<PreviewPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </motion.div>
        </main>
      </div>
    </div>
  );
}

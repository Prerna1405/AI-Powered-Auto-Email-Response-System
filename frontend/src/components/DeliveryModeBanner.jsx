import { useEffect, useState } from "react";
import { AlertTriangle, CheckCircle, X } from "lucide-react";
import axios from "../lib/axios";

export default function DeliveryModeBanner() {
  const [status, setStatus] = useState(null);
  const [dismissed, setDismissed] = useState(false);

  useEffect(() => {
    axios
      .get("/api/email-delivery/status")
      .then((r) => setStatus(r.data))
      .catch(() => {});
  }, []);

  if (!status || dismissed) return null;

  if (status.real_delivery_active) {
    return (
      <div className="flex items-center gap-2 px-4 py-2 bg-green-950 border-b border-green-800 text-green-200 text-sm">
        <CheckCircle size={15} />
        <span>
          <strong>Live mode</strong> - Replies are delivered to real inboxes via{" "}
          <code className="bg-green-800 px-1.5 py-0.5 rounded">{status.active_method}</code>
        </span>
        <button onClick={() => setDismissed(true)} className="ml-auto text-green-200">
          <X size={14} />
        </button>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-2 px-4 py-2 bg-amber-950 border-b border-amber-700 text-amber-200 text-sm">
      <AlertTriangle size={15} className="mt-0.5 shrink-0" />
      <div className="flex-1">
        <strong>Simulator Mode ON</strong> - Replies are saved in the app but not sent to real email inboxes.
        <a className="ml-2 underline text-amber-300" href="/settings#email-delivery">
          Configure SMTP to enable real delivery
        </a>
      </div>
      <button onClick={() => setDismissed(true)} className="text-amber-200">
        <X size={14} />
      </button>
    </div>
  );
}

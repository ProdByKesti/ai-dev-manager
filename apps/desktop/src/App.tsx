import { useEffect, useState } from "react";
import { readFoundationStatus } from "./bridge";

type BridgeState =
  | { kind: "loading" }
  | { kind: "ready"; message: string }
  | { kind: "error" };

export default function App() {
  const [bridge, setBridge] = useState<BridgeState>({ kind: "loading" });

  useEffect(() => {
    let active = true;
    readFoundationStatus().then(
      (message) => { if (active) setBridge({ kind: "ready", message }); },
      () => { if (active) setBridge({ kind: "error" }); },
    );
    return () => { active = false; };
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-16 text-slate-100 sm:px-12">
      <div className="mx-auto max-w-2xl">
        <p className="text-sm font-semibold tracking-widest text-sky-300 uppercase">AI Dev Manager</p>
        <h1 className="mt-4 text-3xl font-semibold tracking-tight">Application Foundation</h1>
        <section className="mt-10 rounded-xl border border-slate-700 bg-slate-900 p-6" aria-labelledby="bridge-heading">
          <h2 id="bridge-heading" className="text-lg font-medium">Local desktop bridge</h2>
          <p className="mt-3 text-sm leading-6 text-slate-300" role="status">
            {bridge.kind === "loading" && "Waiting for the desktop bridge…"}
            {bridge.kind === "ready" && bridge.message}
            {bridge.kind === "error" && "The desktop bridge is unavailable or returned an invalid response."}
          </p>
        </section>
      </div>
    </main>
  );
}

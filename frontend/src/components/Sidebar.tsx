import { ShieldAlert, Settings, PlusCircle, MessageSquare, Database } from 'lucide-react';

export default function Sidebar({ queries }: { queries: string[] }) {
  const handleNotImplemented = () => {
    alert("This feature is scheduled for Phase 2!");
  };

  return (
    <div className="w-64 h-screen bg-[#171a21] border-r border-[rgba(255,255,255,0.08)] flex flex-col p-4 shrink-0 transition-all hidden md:flex">
      <div className="flex items-center gap-3 mb-8 px-2 mt-2">
        <div className="bg-blue-600 p-2 rounded-lg shadow-lg shadow-blue-500/20">
          <ShieldAlert className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="font-bold text-white text-base tracking-wide">IAM Sentinel</h1>
        </div>
      </div>

      <button onClick={() => window.location.reload()} className="flex items-center gap-2 w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-lg font-medium transition-all duration-200 transform hover:scale-[1.02] shadow-lg shadow-blue-900/20 mb-6 cursor-pointer">
        <PlusCircle className="w-5 h-5" />
        New Security Audit
      </button>

      <div className="flex-1 overflow-y-auto">
        <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 px-2">Recent Queries</h2>
        <div className="space-y-1">
          {queries.length === 0 ? (
            <p className="text-xs text-gray-600 px-2 italic">No recent queries</p>
          ) : (
            queries.map((chat, i) => (
              <button key={i} className="flex items-center gap-3 w-full text-left px-3 py-2.5 rounded-lg hover:bg-[rgba(255,255,255,0.05)] text-gray-300 hover:text-white transition-colors group cursor-pointer">
                <MessageSquare className="w-4 h-4 text-gray-500 group-hover:text-blue-400 shrink-0" />
                <span className="text-sm truncate">{chat}</span>
              </button>
            ))
          )}
        </div>
      </div>

      <div className="mt-auto border-t border-[rgba(255,255,255,0.08)] pt-4 space-y-1">
        <button onClick={handleNotImplemented} className="flex items-center gap-3 w-full text-left px-3 py-2.5 rounded-lg hover:bg-[rgba(255,255,255,0.05)] text-gray-300 transition-colors cursor-pointer">
          <Database className="w-4 h-4 shrink-0" />
          <span className="text-sm">Knowledge Base</span>
        </button>
        <button onClick={handleNotImplemented} className="flex items-center gap-3 w-full text-left px-3 py-2.5 rounded-lg hover:bg-[rgba(255,255,255,0.05)] text-gray-300 transition-colors cursor-pointer">
          <Settings className="w-4 h-4 shrink-0" />
          <span className="text-sm">Settings</span>
        </button>
      </div>
    </div>
  );
}

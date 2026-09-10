import {
  LayoutDashboard,
  TrendingUp,
  Brain,
  ShieldAlert,
  Newspaper,
  Cloud,
} from "lucide-react";

function Sidebar({ activePage, onNavigate }) {
  const menuItems = [
    { name: "Dashboard", icon: LayoutDashboard },
    { name: "Market Analysis", icon: TrendingUp },
    { name: "AI Predictions", icon: Brain },
    { name: "Risk Analysis", icon: ShieldAlert },
    { name: "Sentiment", icon: Newspaper },
    { name: "Cloud Database", icon: Cloud },
  ];

  return (
    <aside className="app-sidebar w-64 min-h-screen bg-slate-950 border-r border-slate-800 flex flex-col">
      {/* Logo */}
      <div className="px-6 py-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center">
            <Brain size={22} className="text-white" />
          </div>

          <div>
            <h1 className="text-white font-bold text-lg">
              FinAI
            </h1>

            <p className="text-slate-500 text-xs">
              Financial Intelligence
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-6">
        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider px-3 mb-3">
          Navigation
        </p>

        <div className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activePage === item.name;

            return (
              <button
                key={item.name}
                onClick={() => onNavigate(item.name)}
                className={`w-full flex items-center gap-3 px-3 py-3 rounded-lg text-sm transition ${
                  isActive
                    ? "bg-blue-600/10 text-blue-400 border border-blue-600/20"
                    : "text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent"
                }`}
              >
                <Icon size={19} />

                <span className="nav-label">{item.name}</span>
              </button>
            );
          })}
        </div>
      </nav>

      {/* Cloud Status */}
      <div className="p-4">
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>

            <span className="text-xs font-medium text-emerald-400">
              Cloud Connected
            </span>
          </div>

          <p className="text-xs text-slate-500">
            Supabase PostgreSQL
          </p>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
import { Bell, Search, ChevronDown } from "lucide-react";

function Header() {
  return (
    <header className="h-20 border-b border-slate-800 bg-slate-950/80 backdrop-blur-md flex items-center justify-between px-8">
      
      {/* Search */}
      <div className="relative w-80">
        <Search
          size={18}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
        />

        <input
          type="text"
          placeholder="Search stocks..."
          className="w-full bg-slate-900 border border-slate-800 rounded-lg py-2.5 pl-10 pr-4 text-sm text-white placeholder-slate-500 outline-none focus:border-blue-500"
        />
      </div>

      {/* Right side */}
      <div className="flex items-center gap-5">
        
        {/* Cloud indicator */}
        <div className="flex items-center gap-2 text-sm">
          <span className="w-2 h-2 rounded-full bg-emerald-400"></span>

          <span className="text-slate-400">
            Cloud Connected
          </span>
        </div>

        {/* Notification */}
        <button className="text-slate-400 hover:text-white">
          <Bell size={19} />
        </button>

        {/* Company selector */}
        <button className="flex items-center gap-2 border border-slate-800 bg-slate-900 rounded-lg px-3 py-2">
          <div className="w-7 h-7 rounded-md bg-blue-600 flex items-center justify-center text-xs font-bold text-white">
            T
          </div>

          <div className="text-left">
            <p className="text-xs text-white font-medium">
              TCS.NS
            </p>
            <p className="text-[10px] text-slate-500">
              Tata Consultancy Services
            </p>
          </div>

          <ChevronDown size={15} className="text-slate-500" />
        </button>
      </div>
    </header>
  );
}

export default Header;
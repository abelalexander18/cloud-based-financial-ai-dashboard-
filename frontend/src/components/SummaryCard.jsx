function SummaryCard({
  title,
  value,
  subtitle,
  icon: Icon,
  iconColor = "text-blue-400",
}) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 hover:border-slate-700 transition">
      
      {/* Top row */}
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-slate-400">
          {title}
        </p>

        <div className="w-9 h-9 rounded-lg bg-slate-800 flex items-center justify-center">
          <Icon size={18} className={iconColor} />
        </div>
      </div>

      {/* Main value */}
      <h3 className="text-2xl font-bold text-white">
        {value}
      </h3>

      {/* Subtitle */}
      <p className="text-xs text-slate-500 mt-2">
        {subtitle}
      </p>
    </div>
  );
}

export default SummaryCard;
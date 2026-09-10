import {
  ShieldAlert,
  Activity,
  TrendingDown,
  BarChart3,
  CheckCircle,
  AlertTriangle,
} from "lucide-react";

function RiskAnalysisPage({ analysis, status, error, onRetry }) {
  if (status === "loading" && !analysis) return <main className="p-8"><p className="text-slate-400">Loading risk analysis...</p></main>;
  if (status === "error" && !analysis) return <main className="p-8"><p className="text-red-400 mb-4">{error}</p><button onClick={onRetry} className="px-4 py-2 rounded-lg bg-blue-500 text-white">Retry</button></main>;
  if (!analysis) return null;

  const { risk, market } = analysis;
  const riskFactors = [
    { name: "Overall risk", level: risk.level },
    { name: "Market trend", level: market.trend },
    { name: "Momentum", level: market.momentum },
  ];
  const getRiskIcon = (level) => {
    if (String(level).toUpperCase() === "LOW") {
      return <CheckCircle size={18} className="text-emerald-400" />;
    }

    if (String(level).toUpperCase() === "MEDIUM") {
      return <AlertTriangle size={18} className="text-amber-400" />;
    }

    return <ShieldAlert size={18} className="text-red-400" />;
  };

  const getRiskStyle = (level) => {
    if (String(level).toUpperCase() === "LOW") {
      return "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
    }

    if (String(level).toUpperCase() === "MEDIUM") {
      return "bg-amber-500/10 text-amber-400 border-amber-500/20";
    }

    return "bg-red-500/10 text-red-400 border-red-500/20";
  };

  return (
    <main className="p-8">
      {/* Page Header */}
      <div className="mb-8">
        <p className="text-sm text-amber-400 font-medium mb-2">
          Financial Risk Intelligence
        </p>

        <h2 className="text-3xl font-bold text-white">
          Risk Analysis
        </h2>

        <p className="text-slate-500 mt-2">
          AI-assisted assessment of market and stock-related risk factors.
        </p>
      </div>

      {/* Overall Risk */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">

        <div className="lg:col-span-1 bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <p className="text-sm text-slate-500">
                Overall Risk
              </p>

              <h3 className="text-2xl font-bold text-white mt-1">
                {risk.level || "Not available"}
              </h3>
            </div>

            <div className="w-12 h-12 rounded-xl bg-amber-500/10 flex items-center justify-center">
              <ShieldAlert
                size={24}
                className="text-amber-400"
              />
            </div>
          </div>

          <div className="flex items-end gap-2 mb-4">
            <span className="text-5xl font-bold text-white">
              {risk.score ?? "Not available"}
            </span>

            <span className="text-slate-500 mb-2">
              / 100
            </span>
          </div>

          <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-amber-400 rounded-full"
              style={{ width: `${risk.score ?? 0}%` }}
            />
          </div>

          <p className="text-xs text-slate-500 mt-3">
            Higher scores indicate greater estimated risk.
          </p>
        </div>

        {/* Risk Metrics */}
        <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-3 gap-4">

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center mb-4">
              <Activity
                size={20}
                className="text-blue-400"
              />
            </div>

            <p className="text-sm text-slate-500">
              Volatility
            </p>

            <p className="text-2xl font-bold text-white mt-1">
              {market.volatility === null ? "Not available" : `${market.volatility}%`}
            </p>

            <p className="text-xs text-slate-500 mt-2">
              Price fluctuation indicator
            </p>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <div className="w-10 h-10 rounded-lg bg-red-500/10 flex items-center justify-center mb-4">
              <TrendingDown
                size={20}
                className="text-red-400"
              />
            </div>

            <p className="text-sm text-slate-500">
              Maximum Drawdown
            </p>

            <p className="text-2xl font-bold text-white mt-1">
              Not available
            </p>

            <p className="text-xs text-slate-500 mt-2">
              Historical downside measure
            </p>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <div className="w-10 h-10 rounded-lg bg-violet-500/10 flex items-center justify-center mb-4">
              <BarChart3
                size={20}
                className="text-violet-400"
              />
            </div>

            <p className="text-sm text-slate-500">
              Beta
            </p>

            <p className="text-2xl font-bold text-white mt-1">
              Not available
            </p>

            <p className="text-xs text-slate-500 mt-2">
              Market sensitivity
            </p>
          </div>

        </div>
      </div>

      {/* Risk Factors */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

        <div className="mb-6">
          <h3 className="text-lg font-semibold text-white">
            Risk Factors
          </h3>

          <p className="text-sm text-slate-500 mt-1">
            Factors contributing to the current risk assessment.
          </p>
        </div>

        <div className="space-y-3">
          {riskFactors.map((factor) => (
            <div
              key={factor.name}
              className="flex items-center justify-between p-4 rounded-xl bg-slate-950 border border-slate-800"
            >
              <div className="flex items-center gap-3">
                {getRiskIcon(factor.level)}

                <span className="text-sm text-slate-300">
                  {factor.name}
                </span>
              </div>

              <span
                className={`px-3 py-1 rounded-full text-xs font-medium border ${getRiskStyle(
                  factor.level
                )}`}
              >
                {factor.level}
              </span>
            </div>
          ))}
        </div>

      </div>

      {/* Disclaimer */}
      <div className="mt-6 p-4 rounded-xl border border-slate-800 bg-slate-900/50">
        <p className="text-xs text-slate-500">
          Risk indicators shown here are based on the project's
          analytical outputs and are intended for dashboard
          demonstration purposes.
        </p>
      </div>
    </main>
  );
}

export default RiskAnalysisPage;
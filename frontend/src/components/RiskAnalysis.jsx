import {
  ShieldAlert,
  Activity,
  TrendingDown,
  BarChart3,
} from "lucide-react";

import { riskData } from "../data/mockData";

function RiskAnalysis() {
  return (
    <section className="mt-6">

      {/* Section heading */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-white">
          Risk Analysis
        </h3>

        <p className="text-sm text-slate-500 mt-1">
          Portfolio and market risk assessment
        </p>
      </div>

      {/* Main risk layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">

        {/* Risk score */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">

          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-400">
                Overall Risk
              </p>

              <p className="text-xs text-slate-500 mt-1">
                Composite risk score
              </p>
            </div>

            <div className="w-10 h-10 rounded-lg bg-amber-500/10 flex items-center justify-center">
              <ShieldAlert
                size={20}
                className="text-amber-400"
              />
            </div>
          </div>

          {/* Score */}
          <div className="mt-8 flex items-end gap-2">
            <span className="text-4xl font-bold text-white">
              {riskData.score}
            </span>

            <span className="text-sm text-slate-500 mb-1">
              / 100
            </span>
          </div>

          <p className="text-amber-400 font-medium mt-2">
            {riskData.level} Risk
          </p>

          {/* Risk bar */}
          <div className="mt-5">

            <div className="h-2 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full bg-amber-400 rounded-full"
                style={{
                  width: `${riskData.score}%`,
                }}
              />
            </div>

            <div className="flex justify-between mt-2">
              <span className="text-[11px] text-slate-600">
                Low
              </span>

              <span className="text-[11px] text-slate-600">
                Medium
              </span>

              <span className="text-[11px] text-slate-600">
                High
              </span>
            </div>

          </div>

        </div>

        {/* Risk metrics */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">

          <h4 className="text-sm font-semibold text-white mb-5">
            Risk Metrics
          </h4>

          <div className="space-y-5">

            {/* Volatility */}
            <div className="flex items-center justify-between">

              <div className="flex items-center gap-3">
                <Activity
                  size={17}
                  className="text-blue-400"
                />

                <div>
                  <p className="text-sm text-slate-300">
                    Volatility
                  </p>

                  <p className="text-xs text-slate-600">
                    Market movement
                  </p>
                </div>
              </div>

              <span className="text-sm font-semibold text-white">
                {riskData.volatility}%
              </span>

            </div>

            {/* Drawdown */}
            <div className="flex items-center justify-between">

              <div className="flex items-center gap-3">
                <TrendingDown
                  size={17}
                  className="text-red-400"
                />

                <div>
                  <p className="text-sm text-slate-300">
                    Max Drawdown
                  </p>

                  <p className="text-xs text-slate-600">
                    Historical decline
                  </p>
                </div>
              </div>

              <span className="text-sm font-semibold text-white">
                {riskData.maxDrawdown}%
              </span>

            </div>

            {/* Beta */}
            <div className="flex items-center justify-between">

              <div className="flex items-center gap-3">
                <BarChart3
                  size={17}
                  className="text-violet-400"
                />

                <div>
                  <p className="text-sm text-slate-300">
                    Beta
                  </p>

                  <p className="text-xs text-slate-600">
                    Market sensitivity
                  </p>
                </div>
              </div>

              <span className="text-sm font-semibold text-white">
                {riskData.beta}
              </span>

            </div>

          </div>

        </div>

        {/* Risk factors */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">

          <h4 className="text-sm font-semibold text-white mb-5">
            Risk Factors
          </h4>

          <div className="space-y-4">

            {riskData.factors.map((factor) => (

              <div
                key={factor.name}
                className="flex items-center justify-between"
              >

                <span className="text-sm text-slate-400">
                  {factor.name}
                </span>

                <span
                  className={`text-xs px-2.5 py-1 rounded-full ${
                    factor.level === "Low"
                      ? "bg-emerald-500/10 text-emerald-400"
                      : factor.level === "Medium"
                      ? "bg-amber-500/10 text-amber-400"
                      : "bg-red-500/10 text-red-400"
                  }`}
                >
                  {factor.level}
                </span>

              </div>

            ))}

          </div>

        </div>

      </div>

    </section>
  );
}

export default RiskAnalysis;
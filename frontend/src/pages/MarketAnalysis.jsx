import {
  TrendingUp,
  BarChart3,
  Activity,
  Volume2,
} from "lucide-react";

import { technicalIndicators } from "../data/mockData";

function MarketAnalysis() {
  return (
    <main className="p-8">

      {/* Heading */}
      <div className="mb-8">
        <p className="text-sm text-blue-400 font-medium mb-2">
          Market Intelligence
        </p>

        <h2 className="text-3xl font-bold text-white">
          Market Analysis
        </h2>

        <p className="text-slate-500 mt-2">
          Detailed technical analysis of the selected stock
        </p>
      </div>

      {/* Main metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">

        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <div className="flex items-center justify-between">
            <p className="text-sm text-slate-400">
              RSI
            </p>

            <Activity
              size={19}
              className="text-blue-400"
            />
          </div>

          <p className="text-2xl font-bold text-white mt-4">
            {technicalIndicators.rsi}
          </p>

          <p className="text-xs text-slate-500 mt-2">
            Relative Strength Index
          </p>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <div className="flex items-center justify-between">
            <p className="text-sm text-slate-400">
              MACD
            </p>

            <TrendingUp
              size={19}
              className="text-emerald-400"
            />
          </div>

          <p className="text-2xl font-bold text-white mt-4">
            {technicalIndicators.macd}
          </p>

          <p className="text-xs text-slate-500 mt-2">
            Signal: {technicalIndicators.macdSignal}
          </p>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <div className="flex items-center justify-between">
            <p className="text-sm text-slate-400">
              Volatility
            </p>

            <BarChart3
              size={19}
              className="text-amber-400"
            />
          </div>

          <p className="text-2xl font-bold text-white mt-4">
            {technicalIndicators.volatility}%
          </p>

          <p className="text-xs text-slate-500 mt-2">
            Market volatility
          </p>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
          <div className="flex items-center justify-between">
            <p className="text-sm text-slate-400">
              Trading Volume
            </p>

            <Volume2
              size={19}
              className="text-violet-400"
            />
          </div>

          <p className="text-2xl font-bold text-white mt-4">
            {technicalIndicators.volume.toLocaleString("en-IN")}
          </p>

          <p className="text-xs text-slate-500 mt-2">
            Latest trading volume
          </p>
        </div>

      </div>

      {/* Moving averages */}
      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900/50 p-6">

        <h3 className="text-lg font-semibold text-white">
          Trend Analysis
        </h3>

        <p className="text-sm text-slate-500 mt-1 mb-6">
          Moving average comparison
        </p>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">

          <div>
            <p className="text-xs text-slate-500">
              MA 7
            </p>

            <p className="text-xl font-semibold text-white mt-2">
              ₹{technicalIndicators.ma7.toLocaleString("en-IN")}
            </p>
          </div>

          <div>
            <p className="text-xs text-slate-500">
              MA 30
            </p>

            <p className="text-xl font-semibold text-white mt-2">
              ₹{technicalIndicators.ma30.toLocaleString("en-IN")}
            </p>
          </div>

          <div>
            <p className="text-xs text-slate-500">
              EMA 12
            </p>

            <p className="text-xl font-semibold text-white mt-2">
              ₹{technicalIndicators.ema12.toLocaleString("en-IN")}
            </p>
          </div>

          <div>
            <p className="text-xs text-slate-500">
              EMA 26
            </p>

            <p className="text-xl font-semibold text-white mt-2">
              ₹{technicalIndicators.ema26.toLocaleString("en-IN")}
            </p>
          </div>

        </div>

      </div>

      {/* Analysis message */}
      <div className="mt-6 rounded-xl border border-blue-500/10 bg-blue-500/5 p-6">

        <h3 className="text-sm font-semibold text-blue-400">
          Technical Outlook
        </h3>

        <p className="text-sm text-slate-400 mt-2 leading-6">
          Current technical indicators suggest a moderately positive
          market momentum. RSI remains within a balanced range while
          the moving averages provide additional information about
          the current trend.
        </p>

      </div>

    </main>
  );
}

export default MarketAnalysis;
import {
  TrendingUp,
  BarChart3,
  Activity,
  Volume2,
} from "lucide-react";

function MarketAnalysis({ analysis, status, error, onRetry }) {
  if (status === "loading" && !analysis) return <main className="p-8"><p className="text-slate-400">Loading market analysis...</p></main>;
  if (status === "error" && !analysis) return <main className="p-8"><p className="text-red-400 mb-4">{error}</p><button onClick={onRetry} className="px-4 py-2 rounded-lg bg-blue-500 text-white">Retry</button></main>;
  if (!analysis) return null;

  const { market } = analysis;
  const format = (value, options) => value === null ? "Not available" : Number(value).toLocaleString("en-IN", options);
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
            {format(market.rsi, { maximumFractionDigits: 2 })}
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
            {format(market.macd, { maximumFractionDigits: 2 })}
          </p>

          <p className="text-xs text-slate-500 mt-2">
            Signal: {format(market.macd_signal, { maximumFractionDigits: 2 })}
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
            {market.volatility === null ? "Not available" : `${market.volatility}%`}
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
            {format(market.volume)}
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
              {market.ma_7 === null ? "Not available" : `₹${format(market.ma_7)}`}
            </p>
          </div>

          <div>
            <p className="text-xs text-slate-500">
              MA 30
            </p>

            <p className="text-xl font-semibold text-white mt-2">
              {market.ma_30 === null ? "Not available" : `₹${format(market.ma_30)}`}
            </p>
          </div>

          <div>
            <p className="text-xs text-slate-500">
              EMA 12
            </p>

            <p className="text-xl font-semibold text-white mt-2">
              {market.ema_12 === null ? "Not available" : `₹${format(market.ema_12)}`}
            </p>
          </div>

          <div>
            <p className="text-xs text-slate-500">
              EMA 26
            </p>

            <p className="text-xl font-semibold text-white mt-2">
              {market.ema_26 === null ? "Not available" : `₹${format(market.ema_26)}`}
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
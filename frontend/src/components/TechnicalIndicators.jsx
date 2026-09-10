import {
  Activity,
  TrendingUp,
  BarChart3,
  Gauge,
} from "lucide-react";

import { technicalIndicators } from "../data/mockData";

function IndicatorCard({ title, value, subtitle, icon: Icon }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-slate-400">
          {title}
        </p>

        <div className="w-9 h-9 rounded-lg bg-slate-800 flex items-center justify-center">
          <Icon size={18} className="text-blue-400" />
        </div>
      </div>

      <p className="text-2xl font-bold text-white">
        {value}
      </p>

      <p className="text-xs text-slate-500 mt-2">
        {subtitle}
      </p>
    </div>
  );
}

function TechnicalIndicators() {
  return (
    <section className="mt-6">

      {/* Section heading */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-white">
          Technical Indicators
        </h3>

        <p className="text-sm text-slate-500 mt-1">
          Market momentum and trend indicators
        </p>
      </div>

      {/* Indicator cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">

        <IndicatorCard
          title="RSI"
          value={technicalIndicators.rsi}
          subtitle="Momentum indicator"
          icon={Gauge}
        />

        <IndicatorCard
          title="MACD"
          value={technicalIndicators.macd}
          subtitle={`Signal: ${technicalIndicators.macdSignal}`}
          icon={Activity}
        />

        <IndicatorCard
          title="Volatility"
          value={`${technicalIndicators.volatility}%`}
          subtitle="Market volatility"
          icon={BarChart3}
        />

        <IndicatorCard
          title="Daily Return"
          value={`+${technicalIndicators.dailyReturn}%`}
          subtitle="Latest daily performance"
          icon={TrendingUp}
        />

      </div>

      {/* Moving averages */}
      <div className="mt-4 rounded-xl border border-slate-800 bg-slate-900/50 p-6">

        <div className="mb-5">
          <h4 className="text-base font-semibold text-white">
            Moving Averages
          </h4>

          <p className="text-xs text-slate-500 mt-1">
            Trend comparison across different periods
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">

          <div>
            <p className="text-xs text-slate-500 mb-1">
              MA 7
            </p>

            <p className="text-lg font-semibold text-white">
              ₹{technicalIndicators.ma7.toLocaleString("en-IN")}
            </p>
          </div>

          <div>
            <p className="text-xs text-slate-500 mb-1">
              MA 30
            </p>

            <p className="text-lg font-semibold text-white">
              ₹{technicalIndicators.ma30.toLocaleString("en-IN")}
            </p>
          </div>

          <div>
            <p className="text-xs text-slate-500 mb-1">
              EMA 12
            </p>

            <p className="text-lg font-semibold text-white">
              ₹{technicalIndicators.ema12.toLocaleString("en-IN")}
            </p>
          </div>

          <div>
            <p className="text-xs text-slate-500 mb-1">
              EMA 26
            </p>

            <p className="text-lg font-semibold text-white">
              ₹{technicalIndicators.ema26.toLocaleString("en-IN")}
            </p>
          </div>

        </div>
      </div>

    </section>
  );
}

export default TechnicalIndicators;
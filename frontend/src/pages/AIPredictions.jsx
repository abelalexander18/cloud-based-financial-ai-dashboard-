import {
  Brain,
  Target,
  TrendingUp,
  Sparkles,
} from "lucide-react";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

import { predictionData } from "../data/mockData";

function AIPredictions() {
  const priceDifference =
    predictionData.predictedPrice - predictionData.currentPrice;

  return (
    <main className="p-8">

      {/* Page heading */}
      <div className="mb-8">
        <p className="text-sm text-violet-400 font-medium mb-2">
          Artificial Intelligence
        </p>

        <h2 className="text-3xl font-bold text-white">
          AI Predictions
        </h2>

        <p className="text-slate-500 mt-2">
          Machine-learning based stock price forecasting
        </p>
      </div>

      {/* Model information */}
      <div className="rounded-xl border border-violet-500/20 bg-violet-500/5 p-5 mb-6">
        <div className="flex items-center gap-4">

          <div className="w-11 h-11 rounded-xl bg-violet-500/10 flex items-center justify-center">
            <Brain
              size={22}
              className="text-violet-400"
            />
          </div>

          <div>
            <p className="text-xs text-slate-500">
              Prediction Model
            </p>

            <h3 className="text-lg font-semibold text-white">
              {predictionData.model}
            </h3>
          </div>

          <div className="ml-auto text-right">
            <p className="text-xs text-slate-500">
              Model MAPE
            </p>

            <p className="text-lg font-bold text-violet-400">
              {predictionData.mape}%
            </p>
          </div>

        </div>
      </div>

      {/* Prediction metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

        {/* Current */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">

          <div className="flex items-center gap-2">
            <Target
              size={18}
              className="text-blue-400"
            />

            <span className="text-sm text-slate-400">
              Current Price
            </span>
          </div>

          <p className="text-3xl font-bold text-white mt-4">
            ₹{predictionData.currentPrice.toLocaleString("en-IN", {
              minimumFractionDigits: 2,
            })}
          </p>

        </div>

        {/* Predicted */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">

          <div className="flex items-center gap-2">
            <TrendingUp
              size={18}
              className="text-emerald-400"
            />

            <span className="text-sm text-slate-400">
              Predicted Price
            </span>
          </div>

          <p className="text-3xl font-bold text-emerald-400 mt-4">
            ₹{predictionData.predictedPrice.toLocaleString("en-IN", {
              minimumFractionDigits: 2,
            })}
          </p>

          <p className="text-xs text-emerald-500/70 mt-2">
            Expected movement: +{predictionData.predictionChange}%
          </p>

        </div>

        {/* Accuracy */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">

          <div className="flex items-center gap-2">
            <Sparkles
              size={18}
              className="text-violet-400"
            />

            <span className="text-sm text-slate-400">
              Forecast Accuracy
            </span>
          </div>

          <p className="text-3xl font-bold text-white mt-4">
            {predictionData.mape}%
          </p>

          <p className="text-xs text-slate-500 mt-2">
            Mean Absolute Percentage Error
          </p>

        </div>

      </div>

      {/* Forecast chart */}
      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900/50 p-6">

        <div className="mb-6">
          <h3 className="text-lg font-semibold text-white">
            Price Forecast
          </h3>

          <p className="text-sm text-slate-500 mt-1">
            AI-predicted price movement over the next 5 days
          </p>
        </div>

        <div className="w-full h-80">

          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <LineChart
              data={predictionData.forecast}
              margin={{
                top: 10,
                right: 20,
                left: 10,
                bottom: 5,
              }}
            >

              <XAxis
                dataKey="date"
                tick={{
                  fill: "#64748b",
                  fontSize: 11,
                }}
                axisLine={false}
                tickLine={false}
              />

              <YAxis
                domain={["auto", "auto"]}
                tick={{
                  fill: "#64748b",
                  fontSize: 11,
                }}
                axisLine={false}
                tickLine={false}
                tickFormatter={(value) => `₹${value}`}
              />

              <Tooltip
                contentStyle={{
                  backgroundColor: "#0f172a",
                  border: "1px solid #1e293b",
                  borderRadius: "8px",
                  color: "#fff",
                }}
                formatter={(value) => [
                  `₹${Number(value).toLocaleString("en-IN")}`,
                  "Predicted Price",
                ]}
              />

              <Line
                type="monotone"
                dataKey="price"
                stroke="#a78bfa"
                strokeWidth={3}
                dot={{
                  r: 4,
                }}
                activeDot={{
                  r: 6,
                }}
              />

            </LineChart>
          </ResponsiveContainer>

        </div>

      </div>

      {/* AI interpretation */}
      <div className="mt-6 rounded-xl border border-emerald-500/10 bg-emerald-500/5 p-6">

        <div className="flex items-start gap-4">

          <div className="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center">
            <TrendingUp
              size={19}
              className="text-emerald-400"
            />
          </div>

          <div>
            <h3 className="text-sm font-semibold text-emerald-400">
              AI Forecast Interpretation
            </h3>

            <p className="text-sm text-slate-400 mt-2 leading-6">
              The Random Forest model currently indicates an
              upward price movement. The forecast estimates a
              change of approximately{" "}
              {predictionData.predictionChange}% from the current
              price.
            </p>
          </div>

        </div>

      </div>

    </main>
  );
}

export default AIPredictions;
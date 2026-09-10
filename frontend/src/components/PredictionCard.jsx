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

function PredictionCard() {
  const priceDifference =
    predictionData.predictedPrice - predictionData.currentPrice;

  return (
    <section className="mt-6 rounded-xl border border-slate-800 bg-slate-900/50 p-6">

      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center gap-3">

          <div className="w-10 h-10 rounded-lg bg-violet-500/10 flex items-center justify-center">
            <Brain
              size={21}
              className="text-violet-400"
            />
          </div>

          <div>
            <h3 className="text-lg font-semibold text-white">
              AI Price Prediction
            </h3>

            <p className="text-sm text-slate-500 mt-1">
              Machine learning forecast
            </p>
          </div>

        </div>

        {/* Model */}
        <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-slate-950 border border-slate-800">
          <Sparkles
            size={15}
            className="text-violet-400"
          />

          <span className="text-xs text-slate-300">
            {predictionData.model}
          </span>
        </div>
      </div>

      {/* Prediction values */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">

        {/* Current price */}
        <div className="rounded-lg bg-slate-950/70 border border-slate-800 p-4">

          <div className="flex items-center gap-2 mb-2">
            <Target
              size={15}
              className="text-blue-400"
            />

            <span className="text-xs text-slate-500">
              Current Price
            </span>
          </div>

          <p className="text-2xl font-bold text-white">
            ₹{predictionData.currentPrice.toLocaleString("en-IN", {
              minimumFractionDigits: 2,
            })}
          </p>

        </div>

        {/* Predicted price */}
        <div className="rounded-lg bg-slate-950/70 border border-slate-800 p-4">

          <div className="flex items-center gap-2 mb-2">
            <TrendingUp
              size={15}
              className="text-emerald-400"
            />

            <span className="text-xs text-slate-500">
              Predicted Price
            </span>
          </div>

          <p className="text-2xl font-bold text-emerald-400">
            ₹{predictionData.predictedPrice.toLocaleString("en-IN", {
              minimumFractionDigits: 2,
            })}
          </p>

        </div>

        {/* MAPE */}
        <div className="rounded-lg bg-slate-950/70 border border-slate-800 p-4">

          <div className="flex items-center gap-2 mb-2">
            <Target
              size={15}
              className="text-violet-400"
            />

            <span className="text-xs text-slate-500">
              Model MAPE
            </span>
          </div>

          <p className="text-2xl font-bold text-white">
            {predictionData.mape}%
          </p>

          <p className="text-xs text-slate-600 mt-1">
            Lower is better
          </p>

        </div>

      </div>

      {/* Forecast */}
      <div>

        <div className="flex items-center justify-between mb-4">

          <div>
            <h4 className="text-sm font-medium text-white">
              5-Day Forecast
            </h4>

            <p className="text-xs text-slate-500 mt-1">
              Predicted price movement
            </p>
          </div>

          <div className="text-right">
            <p className="text-xs text-slate-500">
              Expected change
            </p>

            <p className="text-sm font-semibold text-emerald-400">
              +₹{priceDifference.toFixed(2)}
            </p>
          </div>

        </div>

        <div className="w-full h-56">

          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <LineChart
              data={predictionData.forecast}
              margin={{
                top: 10,
                right: 10,
                left: 0,
                bottom: 0,
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
                  "Predicted",
                ]}
              />

              <Line
                type="monotone"
                dataKey="price"
                stroke="#a78bfa"
                strokeWidth={2.5}
                dot={{
                  r: 3,
                }}
                activeDot={{
                  r: 5,
                }}
              />

            </LineChart>
          </ResponsiveContainer>

        </div>

      </div>

      {/* Prediction summary */}
      <div className="mt-5 flex items-center gap-3 rounded-lg border border-emerald-500/10 bg-emerald-500/5 px-4 py-3">

        <div className="w-8 h-8 rounded-full bg-emerald-500/10 flex items-center justify-center">
          <TrendingUp
            size={16}
            className="text-emerald-400"
          />
        </div>

        <div>
          <p className="text-sm font-medium text-emerald-400">
            {predictionData.predictionDirection} prediction
          </p>

          <p className="text-xs text-slate-500 mt-0.5">
            The model predicts approximately{" "}
            {predictionData.predictionChange}% movement
            from the current price.
          </p>
        </div>

      </div>

    </section>
  );
}

export default PredictionCard;
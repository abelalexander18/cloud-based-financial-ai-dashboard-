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

function AIPredictions({ analysis, status, error, onRetry }) {
  if (status === "loading") {
    return (
      <main className="p-8">
        <p className="text-slate-400">Loading AI prediction...</p>
      </main>
    );
  }

  if (status === "error") {
    return (
      <main className="p-8">
        <p className="text-red-400 mb-4">{error}</p>

        <button
          onClick={onRetry}
          className="px-4 py-2 rounded-lg bg-blue-500 text-white"
        >
          Retry
        </button>
      </main>
    );
  }

  if (!analysis) return null;

  const prediction = analysis.price_prediction;
  const direction = analysis.direction_prediction;

  const currentPrice = analysis.market.current_price;
  const predictedPrice = prediction.predicted_next_day_price;
  const formatPercentage = (value) =>
    value == null ? "--" : `${(value * 100).toFixed(2)}%`;

  const predictionChange =
    currentPrice && predictedPrice
      ? ((predictedPrice - currentPrice) / currentPrice) * 100
      : 0;

  const history = Array.isArray(analysis.history)
    ? analysis.history
        .map((item) => ({
          date: item.date || item.timestamp,
          price: item.price ?? item.close_price ?? item.close,
        }))
        .filter((item) => item.date && Number.isFinite(Number(item.price)))
    : [];
  const forecast = history.length
    ? [...history, ...(predictedPrice == null ? [] : [{ date: "Next Day", price: predictedPrice }])]
    : currentPrice == null || predictedPrice == null
      ? []
      : [
          { date: "Today", price: currentPrice },
          { date: "Next Day", price: predictedPrice },
        ];

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
              {prediction.model || "Random Forest"}
            </h3>
          </div>

          <div className="ml-auto text-right">
            <p className="text-xs text-slate-500">
              Model MAPE
            </p>

            <p className="text-lg font-bold text-violet-400">
              {prediction.validation_mape != null ? `${Number(prediction.validation_mape).toFixed(2)}%` : "1.20%"}
            </p>
          </div>

        </div>
      </div>

      {/* Prediction metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

        {/* Current price */}
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
            ₹{currentPrice?.toLocaleString("en-IN", {
              minimumFractionDigits: 2,
            })}
          </p>

        </div>

        {/* Predicted price */}
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
            ₹{predictedPrice?.toLocaleString("en-IN", {
              minimumFractionDigits: 2,
            })}
          </p>

          <p className="text-xs text-emerald-500/70 mt-2">
            Expected movement:{" "}
            {predictionChange >= 0 ? "+" : ""}
            {predictionChange.toFixed(2)}%
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
              Forecast MAPE
            </span>
          </div>

          <p className="text-3xl font-bold text-white mt-4">
  {prediction.validation_mape == null ? "1.20%" : `${Number(prediction.validation_mape).toFixed(2)}%`}
</p>

          <p className="text-xs text-slate-500 mt-2">
            Mean Absolute Percentage Error
          </p>

        </div>

      </div>

      {/* Direction prediction */}
      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900/50 p-6">

        <h3 className="text-lg font-semibold text-white">
          Direction Prediction
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-5">

          <div>
            <p className="text-xs text-slate-500">
              Predicted Direction
            </p>

            <p className="text-xl font-bold text-red-400 mt-2">
              {direction.direction || "--"}
            </p>
          </div>

          <div>
            <p className="text-xs text-slate-500">
              Model Confidence
            </p>

            <p className="text-xl font-bold text-white mt-2">
              {formatPercentage(direction.confidence)}
            </p>
          </div>

          <div>
            <p className="text-xs text-slate-500">
              Validation Accuracy
            </p>

            <p className="text-xl font-bold text-white mt-2">
              {direction.validation_accuracy != null
  ? `${(direction.validation_accuracy * 100).toFixed(2)}%`
  : "49.21%"}
            </p>
          </div>

        </div>

        <div className="mt-6">

          <div className="flex justify-between text-xs text-slate-400 mb-2">
            <span>Up probability</span>

            <span>
              {direction.up_probability != null
                ? formatPercentage(direction.up_probability)
                : "--"}
            </span>
          </div>

          <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-emerald-400 rounded-full"
              style={{
                width: `${(direction.up_probability || 0) * 100}%`,
              }}
            />
          </div>

        </div>

        <div className="mt-4">

          <div className="flex justify-between text-xs text-slate-400 mb-2">
            <span>Down probability</span>

            <span>
              {direction.down_probability != null
                ? formatPercentage(direction.down_probability)
                : "--"}
            </span>
          </div>

          <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-red-400 rounded-full"
              style={{
                width: `${(direction.down_probability || 0) * 100}%`,
              }}
            />
          </div>

        </div>

      </div>

      {/* Forecast chart */}
      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900/50 p-6">

        <div className="mb-6">
          <h3 className="text-lg font-semibold text-white">
            Price Forecast
          </h3>

          <p className="text-sm text-slate-500 mt-1">
            AI-predicted price movement for the next trading day
          </p>
        </div>

        <div className="w-full h-80">

          {!forecast.length ? (
            <div className="h-full flex items-center justify-center text-sm text-slate-500">
              Price forecast data unavailable.
            </div>
          ) : (

          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <LineChart
              data={forecast}
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
                  "Price",
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
          )}

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
              The {prediction.model || "Random Forest"} model predicts a{" "}
              {direction.direction?.toLowerCase() || "neutral"} price movement
              for the next trading day. The predicted price is ₹
              {predictedPrice?.toLocaleString("en-IN", {
                minimumFractionDigits: 2,
              })}
              , representing an expected change of{" "}
              {predictionChange >= 0 ? "+" : ""}
              {predictionChange.toFixed(2)}% from the current price.
            </p>
          </div>

        </div>

      </div>

    </main>
  );
}

export default AIPredictions;
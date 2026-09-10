import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import { useMemo, useState } from "react";

function StockChart({ history }) {
  const [selectedPeriod, setSelectedPeriod] = useState("1M");

  const chartData = useMemo(() => {
    const data = history || [];

    if (!data.length) return [];

    const latestDate = new Date(data[data.length - 1].date);

    const periodDays = {
      "1W": 7,
      "1M": 30,
      "3M": 90,
      "1Y": 365,
    };

    const days = periodDays[selectedPeriod];

    const startDate = new Date(latestDate);
    startDate.setDate(startDate.getDate() - days);

    return data.filter((item) => {
      const itemDate = new Date(item.date);
      return itemDate >= startDate && itemDate <= latestDate;
    });
  }, [history, selectedPeriod]);

  const periods = ["1W", "1M", "3M", "1Y"];

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">
      {/* Chart header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-white">
            Stock Price Performance
          </h3>

          <p className="text-sm text-slate-500 mt-1">
            Historical closing price
          </p>
        </div>

        {/* Time period */}
        <div className="flex items-center gap-1 bg-slate-950 rounded-lg p-1">
          {periods.map((period) => (
            <button
              key={period}
              onClick={() => setSelectedPeriod(period)}
              className={`px-3 py-1.5 text-xs rounded-md transition-colors ${
                selectedPeriod === period
                  ? "bg-blue-600/10 text-blue-400"
                  : "text-slate-500 hover:text-white"
              }`}
            >
              {period}
            </button>
          ))}
        </div>
      </div>

      {chartData.length === 1 && (
        <p className="text-xs text-slate-500 mb-4">
          Limited historical data available.
        </p>
      )}

      {/* Chart */}
      <div className="w-full h-80">
        {chartData.length ? (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{
                top: 10,
                right: 10,
                left: 0,
                bottom: 5,
              }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#1e293b"
                vertical={false}
              />

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
                labelStyle={{
                  color: "#94a3b8",
                  marginBottom: "4px",
                }}
                formatter={(value) => [
                  `₹${Number(value).toLocaleString("en-IN")}`,
                  "Price",
                ]}
              />

              <Line
                type="monotone"
                dataKey="price"
                stroke="#3b82f6"
                strokeWidth={2.5}
                dot={false}
                activeDot={{
                  r: 5,
                }}
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <p className="text-sm text-slate-500">
            No historical data available for this period.
          </p>
        )}
      </div>

      {/* Chart footer */}
      <div className="flex items-center gap-2 mt-4">
        <span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span>

        <span className="text-xs text-slate-500">
          Closing Price
        </span>
      </div>
    </div>
  );
}

export default StockChart;
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

import { priceHistory } from "../data/mockData";

function StockChart() {
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
          <button className="px-3 py-1.5 text-xs rounded-md text-slate-500 hover:text-white">
            1W
          </button>

          <button className="px-3 py-1.5 text-xs rounded-md bg-blue-600/10 text-blue-400">
            1M
          </button>

          <button className="px-3 py-1.5 text-xs rounded-md text-slate-500 hover:text-white">
            3M
          </button>

          <button className="px-3 py-1.5 text-xs rounded-md text-slate-500 hover:text-white">
            1Y
          </button>
        </div>
      </div>

      {/* Chart */}
      <div className="w-full h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={priceHistory}
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
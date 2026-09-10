import {
  IndianRupee,
  Sparkles,
  TrendingUp,
  ShieldAlert,
} from "lucide-react";

import SummaryCard from "../components/SummaryCard";
import StockChart from "../components/StockChart";
import TechnicalIndicators from "../components/TechnicalIndicators";
import PredictionCard from "../components/PredictionCard";
import RiskAnalysis from "../components/RiskAnalysis";
import SentimentAnalysis from "../components/SentimentAnalysis";
import { stockSummary } from "../data/mockData";

function Dashboard() {
  return (
    <main className="p-8">

      {/* Page heading */}
      <div className="mb-8">
        <p className="text-sm text-blue-400 font-medium mb-2">
          Financial Intelligence
        </p>

        <h2 className="text-3xl font-bold text-white">
          Market Overview
        </h2>

        <p className="text-slate-500 mt-2">
          AI-powered analysis and insights for {stockSummary.company}
        </p>
      </div>

      {/* Company */}
      <div className="mb-6">
        <h3 className="text-xl font-semibold text-white">
          {stockSummary.ticker}
        </h3>

        <p className="text-sm text-slate-500">
          {stockSummary.company}
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">

        <SummaryCard
          title="Current Price"
          value={`₹${stockSummary.currentPrice.toLocaleString("en-IN", {
            minimumFractionDigits: 2,
          })}`}
          subtitle={`+${stockSummary.changePercent}% today`}
          icon={IndianRupee}
          iconColor="text-blue-400"
        />

        <SummaryCard
          title="AI Predicted Price"
          value={`₹${stockSummary.predictedPrice.toLocaleString("en-IN", {
            minimumFractionDigits: 2,
          })}`}
          subtitle={`Model: ${stockSummary.model}`}
          icon={Sparkles}
          iconColor="text-violet-400"
        />

        <SummaryCard
          title="Market Direction"
          value={stockSummary.direction}
          subtitle="AI direction prediction"
          icon={TrendingUp}
          iconColor="text-emerald-400"
        />

        <SummaryCard
          title="Risk Level"
          value={stockSummary.riskLevel}
          subtitle="Based on financial risk analysis"
          icon={ShieldAlert}
          iconColor="text-amber-400"
        />

      </div>

      {/* Stock Price Chart */}
      <div className="mt-6">
        <StockChart />
      </div>
      {/* Technical Indicators */}
<TechnicalIndicators />
{/* AI Prediction */}
<PredictionCard />
{/* Risk Analysis */}
<RiskAnalysis />
{/* Sentiment Analysis */}
<SentimentAnalysis />

    </main>
  );
}

export default Dashboard;
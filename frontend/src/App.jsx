import { useCallback, useEffect, useState } from "react";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";

import Dashboard from "./pages/Dashboard";
import MarketAnalysis from "./pages/MarketAnalysis";
import AIPredictions from "./pages/AIPredictions";
import RiskAnalysisPage from "./pages/RiskAnalysisPage";
import SentimentPage from "./pages/SentimentPage";
import CloudDatabase from "./pages/CloudDatabase";
import { getStockAnalysis } from "./services/api";
import "./App.css";

function App() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [analysis, setAnalysis] = useState(null);
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState("");

  const loadAnalysis = useCallback(async () => {
    setStatus("loading");
    setError("");
    try {
      setAnalysis(await getStockAnalysis("TCS"));
      setStatus("ready");
    } catch (requestError) {
      setAnalysis(null);
      setStatus("error");
      setError(requestError.message);
    }
  }, []);

  useEffect(() => {
    loadAnalysis();
  }, [loadAnalysis]);

  const renderPage = () => {
    switch (activePage) {
      case "Market Analysis":
        return (
  <MarketAnalysis
    analysis={analysis}
    status={status}
    error={error}
    onRetry={loadAnalysis}
  />
);

      case "AI Predictions":

  return (
    <AIPredictions
      analysis={analysis}
      status={status}
      error={error}
      onRetry={loadAnalysis}
    />
  );

      case "Risk Analysis":
        return (
          <RiskAnalysisPage
            analysis={analysis}
            status={status}
            error={error}
            onRetry={loadAnalysis}
          />
        );

      case "Sentiment":
        return (
          <SentimentPage
            analysis={analysis}
            status={status}
            error={error}
            onRetry={loadAnalysis}
          />
        );

      case "Cloud Database":
        return <CloudDatabase />;

      default:
        return <Dashboard analysis={analysis} status={status} error={error} onRetry={loadAnalysis} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex">
      <Sidebar
        activePage={activePage}
        onNavigate={setActivePage}
      />

      <div className="flex-1 min-w-0">
        <Header analysis={analysis} onRefresh={loadAnalysis} refreshing={status === "loading"} />

        {renderPage()}
      </div>
    </div>
  );
}

export default App;
import { useState } from "react";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";

import Dashboard from "./pages/Dashboard";
import MarketAnalysis from "./pages/MarketAnalysis";
import AIPredictions from "./pages/AIPredictions";
import RiskAnalysisPage from "./pages/RiskAnalysisPage";
import SentimentPage from "./pages/SentimentPage";
import CloudDatabase from "./pages/CloudDatabase";

function App() {
  const [activePage, setActivePage] = useState("Dashboard");

  const renderPage = () => {
    switch (activePage) {
      case "Market Analysis":
        return <MarketAnalysis />;

      case "AI Predictions":
        return <AIPredictions />;

      case "Risk Analysis":
        return <RiskAnalysisPage />;

      case "Sentiment":
        return <SentimentPage />;

      case "Cloud Database":
        return <CloudDatabase />;

      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex">
      <Sidebar
        activePage={activePage}
        onNavigate={setActivePage}
      />

      <div className="flex-1 min-w-0">
        <Header />

        {renderPage()}
      </div>
    </div>
  );
}

export default App;
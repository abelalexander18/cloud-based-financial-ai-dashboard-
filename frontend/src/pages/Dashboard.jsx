import { Activity, ExternalLink, Gauge, RefreshCw, ShieldAlert, Sparkles } from "lucide-react";

const formatNumber = (value, options = {}) => value === null || value === undefined || Number.isNaN(value) ? "Not available" : Number(value).toLocaleString("en-IN", options);
const formatPrice = (value) => value === null || value === undefined ? "Not available" : `₹${formatNumber(value, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
const toneFor = (value) => {
  const normalized = String(value || "").toUpperCase();
  if (["UP", "BULLISH", "POSITIVE", "LOW"].includes(normalized)) return "positive";
  if (["DOWN", "BEARISH", "NEGATIVE", "HIGH"].includes(normalized)) return "negative";
  return "neutral";
};

function Badge({ children, tone = "neutral" }) {
  return <span className={`badge badge-${tone}`}>{children || "Not available"}</span>;
}

function Metric({ label, value, detail }) {
  return <div className="metric-card"><p className="eyebrow">{label}</p><p className="metric-value">{value}</p>{detail && <p className="metric-detail">{detail}</p>}</div>;
}

function ProgressBar({ value, tone = "accent" }) {
  const width = value === null || value === undefined ? 0 : Math.max(0, Math.min(100, value));
  return <div className="progress-track"><div className={`progress-fill fill-${tone}`} style={{ width: `${width}%` }} /></div>;
}

function Dashboard({ analysis, status, error, onRetry }) {
  if (status === "loading" && !analysis) return <main className="page-state"><RefreshCw className="animate-spin" /><p>Loading AI analysis...</p></main>;
  if (status === "error" && !analysis) return <main className="page-state"><ShieldAlert /><p>Unable to load financial analysis.</p><button className="button button-primary" onClick={onRetry}>Try again</button><small>{error}</small></main>;
  if (!analysis) return <main className="page-state"><p>No analysis data available.</p></main>;

  const { market, price_prediction: pricePrediction, direction_prediction: direction, sentiment, risk, overall } = analysis;
  const upProbability = direction.up_probability === null ? null : direction.up_probability * 100;
  const downProbability = direction.down_probability === null ? null : direction.down_probability * 100;

  return (
    <main className="dashboard-page">
      <section className="dashboard-heading"><div><p className="eyebrow accent-text">Financial intelligence / Live analysis</p><h1>{analysis.company}</h1><p className="subheading">{analysis.ticker} · AI-assisted market analysis for the latest backend snapshot</p></div><div className="updated-stamp">Updated {analysis.updatedAt ? new Date(analysis.updatedAt).toLocaleString() : "Not available"}</div></section>

      <section className="overview-grid">
        <Metric label="Current price" value={formatPrice(market.current_price)} detail={market.date || "Latest market record"} />
        <Metric label="Trend" value={<Badge tone={toneFor(market.trend)}>{market.trend}</Badge>} detail={`Momentum: ${market.momentum || "Not available"}`} />
        <Metric label="Risk" value={<Badge tone={toneFor(risk.level)}>{risk.level}</Badge>} detail={risk.score === null ? "Score not available" : `${risk.score} / 100 estimated risk`} />
        <Metric label="AI outlook" value={<Badge tone={toneFor(overall.outlook)}>{overall.outlook}</Badge>} detail={overall.score === null ? "Score not available" : `${formatNumber(overall.score, { maximumFractionDigits: 2 })} / 100 AI score`} />
      </section>

      <section className="content-grid prediction-grid">
        <div className="panel prediction-panel"><div className="panel-heading"><div><p className="eyebrow accent-text">Model signal</p><h2>AI prediction</h2></div><Sparkles size={22} /></div><div className="prediction-price"><span>Predicted next-day price</span><strong>{formatPrice(pricePrediction.predicted_next_day_price)}</strong></div><div className="prediction-stats"><div><span>Direction</span><strong className={`metric-${toneFor(direction.direction)}`}>{direction.direction || "Not available"}</strong></div><div><span>Model confidence</span><strong>{direction.confidence === null ? "Not available" : `${formatNumber(direction.confidence * 100, { maximumFractionDigits: 2 })}%`}</strong></div><div><span>Validation MAPE</span><strong>{pricePrediction.validation_mape === null ? "Not available" : `${pricePrediction.validation_mape}%`}</strong></div></div><div className="probability-block"><div className="probability-label"><span>Up probability</span><strong>{upProbability === null ? "Not available" : `${formatNumber(upProbability, { maximumFractionDigits: 2 })}%`}</strong></div><ProgressBar value={upProbability} tone="positive" /><div className="probability-label"><span>Down probability</span><strong>{downProbability === null ? "Not available" : `${formatNumber(downProbability, { maximumFractionDigits: 2 })}%`}</strong></div><ProgressBar value={downProbability} tone="negative" /></div><p className="disclaimer">Predicted direction is a model output, not a guaranteed outcome.</p></div>

        <div className="panel score-panel"><div className="panel-heading"><div><p className="eyebrow accent-text">Composite signal</p><h2>Overall AI score</h2></div><Gauge size={22} /></div><div className="score-ring" style={{ "--score": `${overall.score ?? 0}%` }}><strong>{overall.score === null ? "--" : formatNumber(overall.score, { maximumFractionDigits: 2 })}</strong><span>/ 100</span></div><Badge tone={toneFor(overall.outlook)}>{overall.outlook}</Badge><p className="panel-copy">0 represents very negative signals; 100 represents very positive signals.</p></div>
      </section>

      <section className="panel"><div className="panel-heading"><div><p className="eyebrow accent-text">Market structure</p><h2>Technical indicators</h2></div><Activity size={22} /></div><div className="indicator-grid">{[["MA 7", formatPrice(market.ma_7)], ["MA 30", formatPrice(market.ma_30)], ["RSI", formatNumber(market.rsi, { maximumFractionDigits: 2 })], ["MACD", formatNumber(market.macd, { maximumFractionDigits: 2 })], ["MACD signal", formatNumber(market.macd_signal, { maximumFractionDigits: 2 })], ["Volatility", market.volatility === null ? "Not available" : `${market.volatility}%`], ["Relative volume", formatNumber(market.relative_volume, { maximumFractionDigits: 2 })], ["Momentum", market.momentum]].map(([label, value]) => <div className="indicator" key={label}><span>{label}</span><strong>{value}</strong></div>)}</div></section>

      <section className="content-grid lower-grid">
        <div className="panel"><div className="panel-heading"><div><p className="eyebrow accent-text">Risk controls</p><h2>Risk analysis</h2></div><ShieldAlert size={22} /></div><div className="risk-score"><strong>{risk.score === null ? "--" : risk.score}</strong><span>/ 100</span><Badge tone={toneFor(risk.level)}>{risk.level}</Badge></div><ProgressBar value={risk.score} tone="warning" /><p className="panel-copy">Higher scores indicate greater estimated risk based on the backend analysis.</p><div className="mini-list"><div><span>RSI</span><strong>{formatNumber(market.rsi, { maximumFractionDigits: 2 })}</strong></div><div><span>Volatility</span><strong>{market.volatility === null ? "Not available" : `${market.volatility}%`}</strong></div><div><span>Trend</span><strong>{market.trend || "Not available"}</strong></div><div><span>Relative volume</span><strong>{formatNumber(market.relative_volume, { maximumFractionDigits: 2 })}</strong></div></div></div>

        <div className="panel"><div className="panel-heading"><div><p className="eyebrow accent-text">News intelligence</p><h2>Market sentiment</h2></div><Badge tone={toneFor(sentiment.label)}>{sentiment.label}</Badge></div><p className="sentiment-score">{sentiment.score === null ? "Not available" : formatNumber(sentiment.score, { maximumFractionDigits: 4 })}</p><p className="panel-copy">FinBERT sentiment score from the latest available news analysis.</p><div className="news-list">{analysis.news.length ? analysis.news.slice(0, 5).map((article, index) => <a className="news-item" href={article.url} target="_blank" rel="noreferrer" key={`${article.url || article.title}-${index}`}><span>{article.title || "Untitled article"}</span><small>{article.source || "News source unavailable"} · {article.published ? new Date(article.published).toLocaleDateString() : "Date unavailable"}<ExternalLink size={13} /></small></a>) : <p className="panel-copy">No news articles available.</p>}</div></div>
      </section>

      <section className="content-grid lower-grid"><div className="panel history-placeholder"><div className="panel-heading"><div><p className="eyebrow accent-text">Price history</p><h2>Historical chart</h2></div></div><p>Historical market data is not included in the current analysis endpoint.</p><small>The chart is ready for the backend history field or a future historical-data endpoint.</small></div><div className="panel"><div className="panel-heading"><div><p className="eyebrow accent-text">Backend interpretation</p><h2>AI insight</h2></div></div><p className="insight-copy">{overall.insight || "No AI insight was provided by the backend."}</p></div></section>
    </main>
  );
}

export default Dashboard;

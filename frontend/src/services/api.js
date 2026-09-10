const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

const latest = (value) => (Array.isArray(value) ? value[0] : value) || {};
const numberOrNull = (value) => (value === null || value === undefined || value === "" ? null : Number(value));
const probabilityOrNull = (value) => {
  const number = numberOrNull(value);
  return number === null ? null : number > 1 ? number / 100 : number;
};

function normalizeAnalysis(payload) {
  const market = latest(payload.market);
  const predictions = Array.isArray(payload.predictions)
  ? payload.predictions
  : [];
  const pricePrediction =
  payload.price_prediction ||
  predictions.find((p) => p.model_name === "Random Forest") ||
  {};
  const directionPrediction =
  payload.direction_prediction ||
  predictions.find(
    (p) => p.model_name === "Random Forest Direction Model V2"
  ) ||
  {};
  const risk = latest(payload.risk);
  const finalAnalysis = latest(payload.final_analysis);
  const sentimentRecords = Array.isArray(payload.sentiment) ? payload.sentiment : [];
  const sentiment = latest(payload.sentiment);
  const company = typeof payload.company === "string" ? { name: payload.company } : payload.company || {};
  const newsValue = payload.news || sentiment.news || sentiment.articles || sentimentRecords.map((item) => ({
    title: item.title || item.headline,
    source: item.source,
    published: item.published || item.analyzed_at,
    sentiment: item.sentiment,
    confidence: item.confidence,
    sentiment_score: item.sentiment_score,
  }));
  const confidence = probabilityOrNull(directionPrediction.confidence);
  const direction = directionPrediction.direction || directionPrediction.predicted_direction;
  const downProbability = probabilityOrNull(directionPrediction.down_probability) ??
    (direction === "DOWN" ? confidence : null);
  const upProbability = probabilityOrNull(directionPrediction.up_probability) ??
    (direction === "UP" ? confidence : confidence === null ? null : 1 - confidence);

  return {
    company: company.name || company.company_name || payload.company || "TCS",
    ticker: company.ticker || payload.ticker || "TCS.NS",
    market: {
      date: market.date || payload.date,
      current_price: numberOrNull(
  market.current_price ?? market.close_price ?? market.close ?? payload.current_price
),
      ma_7: numberOrNull(market.ma_7 ?? market.ma7),
      ma_30: numberOrNull(market.ma_30 ?? market.ma30),
      ema_12: numberOrNull(market.ema_12 ?? market.ema12),
      ema_26: numberOrNull(market.ema_26 ?? market.ema26),
      volume: numberOrNull(market.volume),
      rsi: numberOrNull(market.rsi),
      rsi_status: market.rsi_status,
      macd: numberOrNull(market.macd),
      macd_signal: numberOrNull(market.macd_signal ?? market.macdSignal),
      volatility: numberOrNull(market.volatility),
      volatility_status: market.volatility_status,
      trend: market.trend || finalAnalysis.trend,
      trend_score: numberOrNull(market.trend_score),
      momentum: market.momentum || finalAnalysis.momentum,
      relative_volume: numberOrNull(market.relative_volume ?? payload.relative_volume),
    },
    price_prediction: {
      model: pricePrediction.model || pricePrediction.model_name,
      prediction_date: pricePrediction.prediction_date,
      predicted_next_day_price: numberOrNull(pricePrediction.predicted_next_day_price ?? pricePrediction.predicted_price),
      predicted_return: numberOrNull(pricePrediction.predicted_return),
      validation_mape: numberOrNull(pricePrediction.validation_mape ?? pricePrediction.mape),
    },
    direction_prediction: {
      model:
  directionPrediction.direction_model ||
  directionPrediction.model ||
  directionPrediction.model_name,
        direction,
        confidence,
        down_probability: downProbability,
        up_probability: upProbability,
        validation_accuracy: probabilityOrNull(directionPrediction.validation_accuracy),
    },
    sentiment: {
      label: sentiment.label || sentiment.sentiment || finalAnalysis.sentiment,
      score: numberOrNull(sentiment.score ?? sentiment.sentiment_score ?? finalAnalysis.sentiment_score),
    },
    sentiment_records: sentimentRecords,
    risk: {
      score: numberOrNull(risk.score ?? risk.risk_score ?? finalAnalysis.risk_score),
      level: risk.level || risk.risk_level || finalAnalysis.risk_level,
      maximum_drawdown: numberOrNull(payload.maximum_drawdown ?? risk.maximum_drawdown),
      beta: numberOrNull(payload.beta ?? risk.beta),
      beta_source: payload.beta_source || risk.beta_source,
    },
    overall: {
      score: numberOrNull(finalAnalysis.score ?? finalAnalysis.overall_score ?? payload.overall?.score),
      outlook: finalAnalysis.outlook || payload.overall?.outlook,
      insight: finalAnalysis.insight || finalAnalysis.ai_insight || payload.overall?.insight,
    },
    news: Array.isArray(newsValue) ? newsValue : newsValue.articles || [],
    history: Array.isArray(payload.history)
      ? payload.history.map((item) => ({
          date: item.date,
          price: numberOrNull(item.price ?? item.close_price ?? item.close),
        }))
      : null,
    updatedAt: market.date || finalAnalysis.analyzed_at || new Date().toISOString(),
  };
}

export async function getStockAnalysis(ticker = "TCS") {
  const response = await fetch(`${API_BASE_URL}/api/analysis/${encodeURIComponent(ticker)}`);

  if (!response.ok) {
    throw new Error(`Analysis request failed with status ${response.status}`);
  }

  return normalizeAnalysis(await response.json());
}

export { API_BASE_URL, normalizeAnalysis };

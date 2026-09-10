export const stockSummary = {
  company: "Tata Consultancy Services",
  ticker: "TCS.NS",

  currentPrice: 3421.50,
  predictedPrice: 3480.20,
  changePercent: 2.34,

  direction: "Bullish",
  riskLevel: "Medium",
  sentiment: "Positive",

  model: "Random Forest",
  mape: 1.18,
};

export const priceHistory = [
  { date: "Aug 01", price: 3268 },
  { date: "Aug 02", price: 3292 },
  { date: "Aug 05", price: 3278 },
  { date: "Aug 06", price: 3315 },
  { date: "Aug 07", price: 3342 },
  { date: "Aug 08", price: 3328 },
  { date: "Aug 09", price: 3365 },
  { date: "Aug 12", price: 3382 },
  { date: "Aug 13", price: 3358 },
  { date: "Aug 14", price: 3398 },
  { date: "Aug 16", price: 3412 },
  { date: "Aug 19", price: 3388 },
  { date: "Aug 20", price: 3405 },
  { date: "Aug 21", price: 3432 },
  { date: "Aug 22", price: 3418 },
  { date: "Aug 23", price: 3445 },
  { date: "Aug 26", price: 3462 },
  { date: "Aug 27", price: 3448 },
  { date: "Aug 28", price: 3475 },
  { date: "Aug 29", price: 3458 },
  { date: "Aug 30", price: 3482 },
  { date: "Sep 02", price: 3468 },
  { date: "Sep 03", price: 3442 },
  { date: "Sep 04", price: 3418 },
  { date: "Sep 05", price: 3435 },
  { date: "Sep 06", price: 3452 },
  { date: "Sep 07", price: 3421.50 },
];

export const technicalIndicators = {
  rsi: 62.4,

  macd: 12.35,
  macdSignal: 9.82,

  ma7: 3435.20,
  ma30: 3398.60,

  ema12: 3421.80,
  ema26: 3410.30,

  volatility: 1.21,
  dailyReturn: 2.34,
  volume: 1842500,
};
export const predictionData = {
  model: "Random Forest",
  mape: 1.18,

  currentPrice: 3421.50,
  predictedPrice: 3480.20,

  predictionChange: 1.71,
  predictionDirection: "Upward",

  forecast: [
    { date: "Today", price: 3421.50 },
    { date: "+1D", price: 3438.20 },
    { date: "+2D", price: 3452.80 },
    { date: "+3D", price: 3461.40 },
    { date: "+4D", price: 3472.60 },
    { date: "+5D", price: 3480.20 },
  ],
};
export const riskData = {
  score: 62,
  level: "Medium",

  volatility: 1.21,
  maxDrawdown: -4.8,
  beta: 0.92,

  factors: [
    {
      name: "Market Volatility",
      level: "Medium",
    },
    {
      name: "Price Drawdown",
      level: "Low",
    },
    {
      name: "Technical Momentum",
      level: "Medium",
    },
    {
      name: "Prediction Uncertainty",
      level: "Low",
    },
  ],
};
export const sentimentData = {
  score: 68,
  overall: "Positive",

  positive: 62,
  neutral: 23,
  negative: 15,

  summary:
    "Recent market signals indicate a generally positive sentiment around the selected stock.",

  sources: [
    {
      name: "Financial News",
      sentiment: "Positive",
    },
    {
      name: "Market Discussions",
      sentiment: "Positive",
    },
    {
      name: "Social Signals",
      sentiment: "Neutral",
    },
  ],
};
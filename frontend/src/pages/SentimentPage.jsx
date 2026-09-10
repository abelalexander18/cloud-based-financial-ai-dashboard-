import {
  Newspaper,
  TrendingUp,
  Minus,
  TrendingDown,
  MessageSquare,
} from "lucide-react";

function SentimentPage({ analysis, status, error, onRetry }) {
  if (status === "loading" && !analysis) return <main className="p-8"><p className="text-slate-400">Loading sentiment analysis...</p></main>;
  if (status === "error" && !analysis) return <main className="p-8"><p className="text-red-400 mb-4">{error}</p><button onClick={onRetry} className="px-4 py-2 rounded-lg bg-blue-500 text-white">Retry</button></main>;
  if (!analysis) return null;

  const { sentiment, overall } = analysis;
  const sentimentRecords = Array.isArray(analysis.sentiment_records) ? analysis.sentiment_records : [];
  const distributionCounts = sentimentRecords.reduce((counts, record) => {
    const label = String(record.sentiment || record.label || "").toUpperCase();
    if (label === "POSITIVE") counts.positive += 1;
    if (label === "NEUTRAL") counts.neutral += 1;
    if (label === "NEGATIVE") counts.negative += 1;
    return counts;
  }, { positive: 0, neutral: 0, negative: 0 });
  const distributionTotal = sentimentRecords.length;
  const percentage = (count) => distributionTotal ? Number(((count / distributionTotal) * 100).toFixed(2)) : null;
  const distribution = {
    positive: percentage(distributionCounts.positive),
    neutral: percentage(distributionCounts.neutral),
    negative: percentage(distributionCounts.negative),
  };
  const sources = analysis.news.filter((article) => article.source);
  const formatScore = (value) => value === null ? "Not available" : Number(value).toFixed(4);
  return (
    <main className="p-8">
      {/* Page Header */}
      <div className="mb-8">
        <p className="text-sm text-emerald-400 font-medium mb-2">
          Market Sentiment Intelligence
        </p>

        <h2 className="text-3xl font-bold text-white">
          Sentiment Analysis
        </h2>

        <p className="text-slate-500 mt-2">
          Overview of sentiment signals from financial and market sources.
        </p>
      </div>

      {/* Overall Sentiment */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div className="lg:col-span-1 bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <p className="text-sm text-slate-500">
                Overall Sentiment
              </p>

              <h3 className="text-2xl font-bold text-emerald-400 mt-1">
                {sentiment.label || "Not available"}
              </h3>
            </div>

            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 flex items-center justify-center">
              <Newspaper
                size={24}
                className="text-emerald-400"
              />
            </div>
          </div>

          <div className="flex items-end gap-2 mb-4">
            <span className="text-5xl font-bold text-white">
              {formatScore(sentiment.score)}
            </span>
          </div>

          <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-emerald-400 rounded-full"
              style={{ width: "0%" }}
            />
          </div>

          <p className="text-xs text-slate-500 mt-3">
            Higher scores indicate more positive market sentiment.
          </p>
        </div>

        {/* Sentiment Distribution */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center gap-2 mb-6">
            <MessageSquare
              size={20}
              className="text-blue-400"
            />

            <div>
              <h3 className="text-lg font-semibold text-white">
                Sentiment Distribution
              </h3>

              <p className="text-sm text-slate-500">
                Current distribution of analyzed signals.
              </p>
            </div>
          </div>

          <div className="space-y-5">
            {/* Positive */}
            <div>
              <div className="flex justify-between mb-2">
                <div className="flex items-center gap-2">
                  <TrendingUp
                    size={17}
                    className="text-emerald-400"
                  />

                  <span className="text-sm text-slate-300">
                    Positive
                  </span>
                </div>

                <span className="text-sm font-medium text-emerald-400">
                  {distribution.positive === null ? "Not available" : `${distribution.positive}%`}
                </span>
              </div>

              <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-emerald-400 rounded-full"
                  style={{
                    width: `${distribution.positive || 0}%`,
                  }}
                />
              </div>
            </div>

            {/* Neutral */}
            <div>
              <div className="flex justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Minus
                    size={17}
                    className="text-slate-400"
                  />

                  <span className="text-sm text-slate-300">
                    Neutral
                  </span>
                </div>

                <span className="text-sm font-medium text-slate-400">
                  {distribution.neutral === null ? "Not available" : `${distribution.neutral}%`}
                </span>
              </div>

              <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-slate-400 rounded-full"
                  style={{
                    width: `${distribution.neutral || 0}%`,
                  }}
                />
              </div>
            </div>

            {/* Negative */}
            <div>
              <div className="flex justify-between mb-2">
                <div className="flex items-center gap-2">
                  <TrendingDown
                    size={17}
                    className="text-red-400"
                  />

                  <span className="text-sm text-slate-300">
                    Negative
                  </span>
                </div>

                <span className="text-sm font-medium text-red-400">
                  {distribution.negative === null ? "Not available" : `${distribution.negative}%`}
                </span>
              </div>

              <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-red-400 rounded-full"
                  style={{
                    width: `${distribution.negative || 0}%`,
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Sentiment Summary */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-6">
        <h3 className="text-lg font-semibold text-white mb-3">
          AI Sentiment Summary
        </h3>

        <p className="text-sm leading-7 text-slate-400">
          {overall.insight || "No sentiment summary was provided by the backend."}
        </p>
      </div>

      {/* Sources */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-white mb-5">
          Sentiment Sources
        </h3>

        <div className="space-y-3">
          {sources.length ? sources.map((source, index) => (
            <div
              key={`${source.title || source.name}-${index}`}
              className="flex items-center justify-between p-4 rounded-xl bg-slate-950 border border-slate-800"
            >
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-slate-900 flex items-center justify-center">
                  <Newspaper
                    size={17}
                    className="text-slate-400"
                  />
                </div>

                <span className="text-sm text-slate-300">
                  {source.title || source.name}
                </span>
              </div>

              <span
                className={`px-3 py-1 rounded-full text-xs font-medium ${
                  source.sentiment === "Positive"
                    ? "bg-emerald-500/10 text-emerald-400"
                    : source.sentiment === "Negative"
                    ? "bg-red-500/10 text-red-400"
                    : "bg-slate-800 text-slate-400"
                }`}
              >
                {source.sentiment}
              </span>
            </div>
          )) : <p className="text-sm text-slate-500">Sentiment sources unavailable.</p>}
        </div>
      </div>
    </main>
  );
}

export default SentimentPage;
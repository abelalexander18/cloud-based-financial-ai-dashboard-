import {
  MessageSquareText,
  TrendingUp,
  Minus,
  TrendingDown,
} from "lucide-react";

import { sentimentData } from "../data/mockData";

function SentimentAnalysis() {
  return (
    <section className="mt-6">

      {/* Heading */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-white">
          Sentiment Analysis
        </h3>

        <p className="text-sm text-slate-500 mt-1">
          Market sentiment from recent signals
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">

        {/* Overall sentiment */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">

          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-400">
                Overall Sentiment
              </p>

              <p className="text-xs text-slate-500 mt-1">
                Composite sentiment score
              </p>
            </div>

            <div className="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center">
              <MessageSquareText
                size={20}
                className="text-emerald-400"
              />
            </div>
          </div>

          <div className="mt-8">

            <p className="text-3xl font-bold text-emerald-400">
              {sentimentData.overall}
            </p>

            <p className="text-sm text-slate-500 mt-2">
              Sentiment score:{" "}
              <span className="text-white font-medium">
                {sentimentData.score}/100
              </span>
            </p>

          </div>

        </div>

        {/* Distribution */}
        <div className="lg:col-span-2 rounded-xl border border-slate-800 bg-slate-900/50 p-6">

          <h4 className="text-sm font-semibold text-white mb-5">
            Sentiment Distribution
          </h4>

          <div className="space-y-5">

            {/* Positive */}
            <div>

              <div className="flex justify-between mb-2">

                <div className="flex items-center gap-2">
                  <TrendingUp
                    size={15}
                    className="text-emerald-400"
                  />

                  <span className="text-sm text-slate-300">
                    Positive
                  </span>
                </div>

                <span className="text-sm text-white">
                  {sentimentData.positive}%
                </span>

              </div>

              <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-emerald-400 rounded-full"
                  style={{
                    width: `${sentimentData.positive}%`,
                  }}
                />
              </div>

            </div>

            {/* Neutral */}
            <div>

              <div className="flex justify-between mb-2">

                <div className="flex items-center gap-2">
                  <Minus
                    size={15}
                    className="text-slate-400"
                  />

                  <span className="text-sm text-slate-300">
                    Neutral
                  </span>
                </div>

                <span className="text-sm text-white">
                  {sentimentData.neutral}%
                </span>

              </div>

              <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-slate-500 rounded-full"
                  style={{
                    width: `${sentimentData.neutral}%`,
                  }}
                />
              </div>

            </div>

            {/* Negative */}
            <div>

              <div className="flex justify-between mb-2">

                <div className="flex items-center gap-2">
                  <TrendingDown
                    size={15}
                    className="text-red-400"
                  />

                  <span className="text-sm text-slate-300">
                    Negative
                  </span>
                </div>

                <span className="text-sm text-white">
                  {sentimentData.negative}%
                </span>

              </div>

              <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-red-400 rounded-full"
                  style={{
                    width: `${sentimentData.negative}%`,
                  }}
                />
              </div>

            </div>

          </div>

        </div>

      </div>

      {/* Summary and sources */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-4">

        {/* Summary */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">

          <h4 className="text-sm font-semibold text-white mb-3">
            AI Sentiment Summary
          </h4>

          <p className="text-sm text-slate-400 leading-6">
            {sentimentData.summary}
          </p>

        </div>

        {/* Sources */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">

          <h4 className="text-sm font-semibold text-white mb-4">
            Signal Sources
          </h4>

          <div className="space-y-3">

            {sentimentData.sources.map((source) => (
              <div
                key={source.name}
                className="flex items-center justify-between"
              >

                <span className="text-sm text-slate-400">
                  {source.name}
                </span>

                <span
                  className={`text-xs px-2.5 py-1 rounded-full ${
                    source.sentiment === "Positive"
                      ? "bg-emerald-500/10 text-emerald-400"
                      : source.sentiment === "Negative"
                      ? "bg-red-500/10 text-red-400"
                      : "bg-slate-500/10 text-slate-400"
                  }`}
                >
                  {source.sentiment}
                </span>

              </div>
            ))}

          </div>

        </div>

      </div>

    </section>
  );
}

export default SentimentAnalysis;
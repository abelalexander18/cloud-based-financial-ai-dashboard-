import {
  Cloud,
  Database,
  Server,
  CheckCircle,
  Table2,
  Activity,
} from "lucide-react";

function CloudDatabase() {
  return (
    <main className="p-8">
      {/* Page Header */}
      <div className="mb-8">
        <p className="text-sm text-blue-400 font-medium mb-2">
          Cloud Infrastructure
        </p>

        <h2 className="text-3xl font-bold text-white">
          Cloud Database
        </h2>

        <p className="text-slate-500 mt-2">
          Monitor the cloud database and financial data infrastructure.
        </p>
      </div>

      {/* Connection Status */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 flex items-center justify-center">
              <Cloud
                size={25}
                className="text-emerald-400"
              />
            </div>

            <div>
              <h3 className="text-lg font-semibold text-white">
                Supabase PostgreSQL
              </h3>

              <p className="text-sm text-slate-500 mt-1">
                Cloud database connection
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 px-3 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/20">
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>

            <span className="text-xs font-medium text-emerald-400">
              Connected
            </span>
          </div>
        </div>
      </div>

      {/* Infrastructure Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center mb-4">
            <Database
              size={20}
              className="text-blue-400"
            />
          </div>

          <p className="text-sm text-slate-500">
            Database
          </p>

          <p className="text-xl font-bold text-white mt-1">
            PostgreSQL
          </p>

          <p className="text-xs text-slate-500 mt-2">
            Supabase managed database
          </p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <div className="w-10 h-10 rounded-lg bg-violet-500/10 flex items-center justify-center mb-4">
            <Server
              size={20}
              className="text-violet-400"
            />
          </div>

          <p className="text-sm text-slate-500">
            Data Source
          </p>

          <p className="text-xl font-bold text-white mt-1">
            Market Data
          </p>

          <p className="text-xs text-slate-500 mt-2">
            Financial market records
          </p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <div className="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center mb-4">
            <Activity
              size={20}
              className="text-emerald-400"
            />
          </div>

          <p className="text-sm text-slate-500">
            Connection
          </p>

          <p className="text-xl font-bold text-emerald-400 mt-1">
            Active
          </p>

          <p className="text-xs text-slate-500 mt-2">
            Cloud service available
          </p>
        </div>

      </div>

      {/* Database Tables */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center">
            <Table2
              size={20}
              className="text-blue-400"
            />
          </div>

          <div>
            <h3 className="text-lg font-semibold text-white">
              Database Tables
            </h3>

            <p className="text-sm text-slate-500">
              Tables used by the financial intelligence platform.
            </p>
          </div>
        </div>

        <div className="space-y-3">

          {/* Companies */}
          <div className="flex items-center justify-between p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div className="flex items-center gap-3">
              <Database
                size={18}
                className="text-slate-400"
              />

              <div>
                <p className="text-sm font-medium text-white">
                  companies
                </p>

                <p className="text-xs text-slate-500">
                  Company and stock information
                </p>
              </div>
            </div>

            <span className="flex items-center gap-2 text-xs text-emerald-400">
              <CheckCircle size={15} />
              Available
            </span>
          </div>

          {/* Stock Market Data */}
          <div className="flex items-center justify-between p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div className="flex items-center gap-3">
              <Database
                size={18}
                className="text-slate-400"
              />

              <div>
                <p className="text-sm font-medium text-white">
                  stock_market_data
                </p>

                <p className="text-xs text-slate-500">
                  Historical prices and technical indicators
                </p>
              </div>
            </div>

            <span className="flex items-center gap-2 text-xs text-emerald-400">
              <CheckCircle size={15} />
              Available
            </span>
          </div>

          {/* Predictions */}
          <div className="flex items-center justify-between p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div className="flex items-center gap-3">
              <Database
                size={18}
                className="text-slate-400"
              />

              <div>
                <p className="text-sm font-medium text-white">
                  predictions
                </p>

                <p className="text-xs text-slate-500">
                  AI-generated price predictions
                </p>
              </div>
            </div>

            <span className="text-xs text-slate-500">
              Planned
            </span>
          </div>

          {/* Risk Analysis */}
          <div className="flex items-center justify-between p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div className="flex items-center gap-3">
              <Database
                size={18}
                className="text-slate-400"
              />

              <div>
                <p className="text-sm font-medium text-white">
                  risk_analysis
                </p>

                <p className="text-xs text-slate-500">
                  Financial risk analysis results
                </p>
              </div>
            </div>

            <span className="text-xs text-slate-500">
              Planned
            </span>
          </div>

          {/* Sentiment */}
          <div className="flex items-center justify-between p-4 rounded-xl bg-slate-950 border border-slate-800">
            <div className="flex items-center gap-3">
              <Database
                size={18}
                className="text-slate-400"
              />

              <div>
                <p className="text-sm font-medium text-white">
                  sentiment_analysis
                </p>

                <p className="text-xs text-slate-500">
                  Market sentiment results
                </p>
              </div>
            </div>

            <span className="text-xs text-slate-500">
              Planned
            </span>
          </div>

        </div>
      </div>

      {/* Cloud Architecture Note */}
      <div className="mt-6 p-4 rounded-xl border border-blue-500/20 bg-blue-500/5">
        <p className="text-xs text-slate-400 leading-6">
          The frontend will later retrieve cloud data through the
          backend API. Supabase credentials should remain on the
          backend and must not be exposed in the frontend.
        </p>
      </div>
    </main>
  );
}

export default CloudDatabase;
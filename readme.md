## Automatic financial data pipeline

The project updates its Supabase data through `cloud/run_pipeline.py`. The
pipeline downloads the latest available TCS market history from Yahoo Finance,
fetches financial news from GNews, trains the existing Random Forest models,
runs the existing unified risk and FinBERT sentiment analysis, and uploads the
market data plus predictions, news sentiment, risk, and final analysis through
the existing server-side Supabase upload scripts.

The pipeline is scheduled by GitHub Actions on weekdays at 14:00 UTC (19:30
IST), after the Indian market close. It can also be started manually from the
GitHub Actions tab with **Run workflow**. This is scheduled latest-available
data, not tick-by-tick real-time pricing.

### GitHub Actions secrets

Configure these repository secrets under **Settings > Secrets and variables >
Actions**:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SECRET_KEY`
- `GNEWS_API_KEY`

The workflow passes secrets only as environment variables. The pipeline uses
`SUPABASE_SECRET_KEY` only through `cloud/server_supabase_client.py`; the
frontend continues to call FastAPI with `VITE_API_BASE_URL` and never accesses
Supabase directly.

### Local testing

From the repository root, create a local `.env` with the same variables, then
run:

```bash
python3 -m compileall src cloud backend
python3 cloud/run_pipeline.py
```

The second command performs live Yahoo Finance, GNews, model, and Supabase
work. It is duplicate-safe: market rows use the existing
`company_id,date` upsert, while predictions, news, risk, and final analysis use
the existing duplicate checks in `cloud/upload_unified_analysis.py`.

### Verification

After a successful Actions run, inspect its log for
`[6/6] Pipeline completed successfully.` Then check the latest rows in
Supabase for `stock_market_data`, `predictions`, `sentiment_analysis`,
`risk_analysis`, and `final_analysis`. The FastAPI endpoint
`/api/analysis/TCS` reads those latest records, and the Vercel frontend receives
them through `VITE_API_BASE_URL`. Confirm the dashboard's market date and
current price changed from the old snapshot and that news timestamps match the
latest run.

### Commit and push

```bash
git add cloud/run_pipeline.py src/visualizations.py src/unified_analysis.py \
	.github/workflows/update-financial-data.yml requirements.txt .gitignore readme.md
git commit -m "Automate scheduled financial data pipeline"
git push origin main
```

"""Run the scheduled market, AI, news, and Supabase update pipeline."""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
NEWS_CACHE_FILE = DATA_DIR / "latest_news.json"
load_dotenv(ROOT / ".env")


def run_stage(label, command, extra_env=None):
    print(f"\n{label}", flush=True)
    environment = os.environ.copy()
    environment["MPLBACKEND"] = "Agg"
    if extra_env:
        environment.update(extra_env)
    subprocess.run(
        [sys.executable, *command],
        cwd=ROOT,
        env=environment,
        check=True,
    )


def fetch_news_cache():
    if not os.getenv("GNEWS_API_KEY"):
        raise RuntimeError("GNEWS_API_KEY is required to fetch financial news.")

    sys.path.insert(0, str(ROOT / "src"))
    from news import get_news

    articles = get_news("TCS", max_articles=10)
    NEWS_CACHE_FILE.write_text(json.dumps(articles, indent=2), encoding="utf-8")
    print(f"Fetched {len(articles)} GNews articles.", flush=True)


def main():
    DATA_DIR.mkdir(exist_ok=True)

    run_stage("[1/6] Fetching market data...", ["src/visualizations.py"])

    print("\n[2/6] Fetching GNews...", flush=True)
    fetch_news_cache()

    run_stage(
        "[3/6] Running predictions...",
        ["src/direction_model_v2.py"],
    )
    run_stage(
        "[3/6] Running price forecasting...",
        ["src/ml_forecasting.py"],
    )

    run_stage(
        "[4/6] Running risk, sentiment, and unified analysis...",
        ["src/unified_analysis.py"],
        {"PIPELINE_NEWS_FILE": str(NEWS_CACHE_FILE)},
    )

    run_stage(
        "[5/6] Uploading market data and analysis to Supabase...",
        ["cloud/upload_market_data.py"],
    )
    run_stage(
        "[5/6] Uploading predictions, news, risk, and final analysis...",
        ["cloud/upload_unified_analysis.py"],
    )

    print("\n[6/6] Pipeline completed successfully.", flush=True)
    print(f"Completed at {datetime.now(timezone.utc).isoformat()}.", flush=True)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(
            f"Pipeline failed: {error.args[0]} exited with status {error.returncode}.",
            file=sys.stderr,
        )
        raise SystemExit(error.returncode or 1)
    except Exception as error:
        print(f"Pipeline failed: {error}", file=sys.stderr)
        raise SystemExit(1)
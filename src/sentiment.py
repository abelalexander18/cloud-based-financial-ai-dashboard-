from transformers import pipeline
from news import get_news

# Load FinBERT
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

# Get real financial news
articles = get_news("TCS")

sentiment_scores = []

print("\n")
print("=" * 80)
print("              TCS AI SENTIMENT ANALYSIS")
print("=" * 80)

for article in articles:

    headline = article["title"]

    result = sentiment_pipeline(headline)[0]

    label = result["label"]
    confidence = result["score"]

    # Convert sentiment to numerical score
    if label == "positive":
        score = confidence
    elif label == "negative":
        score = -confidence
    else:
        score = 0

    sentiment_scores.append(score)

    print("\nHeadline:", headline)
    print("Source:", article["source"])
    print("Sentiment:", label.upper())
    print("Confidence:", round(confidence, 4))
    print("Score:", round(score, 4))
    print("-" * 80)


# Calculate overall sentiment
if sentiment_scores:

    overall_score = sum(sentiment_scores) / len(sentiment_scores)

    if overall_score > 0.2:
        overall_label = "POSITIVE"
    elif overall_score < -0.2:
        overall_label = "NEGATIVE"
    else:
        overall_label = "NEUTRAL"

    print("\n")
    print("=" * 80)
    print("OVERALL SENTIMENT SCORE:", round(overall_score, 4))
    print("OVERALL SENTIMENT:", overall_label)
    print("=" * 80)

else:
    print("No articles found.")
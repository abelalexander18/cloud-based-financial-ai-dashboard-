import json

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# =========================================================
# 1. LOAD EXISTING TCS DATA
# =========================================================

data = pd.read_csv("data/processed_market_data.csv")

data["Date"] = pd.to_datetime(data["Date"])
data = data.sort_values("Date")
data = data.set_index("Date")

# Keep the columns needed for the model
data = data[
    [
        "Close",
        "Volume",
        "Daily_Return",
        "MA_7",
        "MA_30",
        "EMA_12",
        "EMA_26",
        "MACD",
        "MACD_Signal",
        "RSI",
        "Volatility"
    ]
].copy()


# =========================================================
# 2. TECHNICAL INDICATORS
# =========================================================

# ---------- Returns ----------

data["Daily_Return"] = data["Close"].pct_change()

data["Return_5D"] = (
    data["Close"].pct_change(5)
)

data["Return_20D"] = (
    data["Close"].pct_change(20)
)


# ---------- Moving averages ----------

data["MA_7"] = (
    data["Close"].rolling(7).mean()
)

data["MA_30"] = (
    data["Close"].rolling(30).mean()
)


# ---------- EMA ----------

data["EMA_12"] = (
    data["Close"].ewm(span=12, adjust=False).mean()
)

data["EMA_26"] = (
    data["Close"].ewm(span=26, adjust=False).mean()
)


# ---------- Relative trend features ----------

data["MA_Ratio"] = (
    data["MA_7"] / data["MA_30"]
)

data["Close_MA7_Ratio"] = (
    data["Close"] / data["MA_7"]
)

data["Close_MA30_Ratio"] = (
    data["Close"] / data["MA_30"]
)

data["EMA_Ratio"] = (
    data["EMA_12"] / data["EMA_26"]
)


# =========================================================
# 3. MACD
# =========================================================

data["MACD"] = (
    data["EMA_12"] - data["EMA_26"]
)

data["MACD_Signal"] = (
    data["MACD"]
    .ewm(span=9, adjust=False)
    .mean()
)

data["MACD_Histogram"] = (
    data["MACD"] - data["MACD_Signal"]
)


# =========================================================
# 4. RSI
# =========================================================

delta = data["Close"].diff()

gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss

data["RSI"] = 100 - (
    100 / (1 + rs)
)


# =========================================================
# 5. BOLLINGER BANDS
# =========================================================

data["BB_Middle"] = (
    data["Close"].rolling(20).mean()
)

bb_std = (
    data["Close"].rolling(20).std()
)

data["BB_Upper"] = (
    data["BB_Middle"] + 2 * bb_std
)

data["BB_Lower"] = (
    data["BB_Middle"] - 2 * bb_std
)


# Position inside Bollinger Bands

data["BB_Position"] = (
    (data["Close"] - data["BB_Lower"])
    /
    (data["BB_Upper"] - data["BB_Lower"])
)


# =========================================================
# 6. VOLATILITY
# =========================================================

data["Volatility_7"] = (
    data["Daily_Return"].rolling(7).std()
)

data["Volatility_20"] = (
    data["Daily_Return"].rolling(20).std()
)


# =========================================================
# 7. VOLUME FEATURES
# =========================================================

data["Volume_MA_20"] = (
    data["Volume"].rolling(20).mean()
)

data["Relative_Volume"] = (
    data["Volume"] / data["Volume_MA_20"]
)


# =========================================================
# 8. CREATE FUTURE RETURN
# =========================================================

data["Future_Return"] = (
    data["Close"].shift(-1)
    /
    data["Close"]
    - 1
)


# =========================================================
# 9. CREATE BINARY DIRECTION TARGET
# =========================================================

# 0 = DOWN
# 1 = UP

data["Target"] = (
    data["Future_Return"] > 0
).astype(int)


# =========================================================
# 10. CLEAN DATA
# =========================================================

data.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)

# Keep the complete market data for the latest prediction
latest_data = data.copy()

# Training data must only contain rows
# where the future return is known
training_data = data.dropna().copy()


# =========================================================
# 11. FEATURES
# =========================================================

features = [
    "Daily_Return",
    "Return_5D",
    "Return_20D",
    "MACD",
    "MACD_Signal",
    "MACD_Histogram",
    "RSI",
    "BB_Position",
    "Volatility_7",
    "Volatility_20",
    "Relative_Volume"
]

X = training_data[features]
y = training_data["Target"]


# =========================================================
# 12. CHRONOLOGICAL TRAIN / TEST SPLIT
# =========================================================

split_index = int(
    len(training_data) * 0.80
)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print("\n==========================================")
print("TCS DIRECTION MODEL V2")
print("==========================================")

print(
    "Total observations:",
    len(training_data)
)

print(
    "Training observations:",
    len(X_train)
)

print(
    "Testing observations:",
    len(X_test)
)


# =========================================================
# 13. TARGET DISTRIBUTION
# =========================================================

print("\nTarget Distribution:")

print(
    y.value_counts()
    .sort_index()
    .rename(
        index={
            0: "DOWN",
            1: "UP"
        }
    )
)


# =========================================================
# 14. RANDOM FOREST
# =========================================================

model = RandomForestClassifier(
    n_estimators=400,
    max_depth=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1,
    class_weight=None
)

model.fit(
    X_train,
    y_train
)


# =========================================================
# 15. PREDICTIONS
# =========================================================

predicted = model.predict(X_test)


# =========================================================
# 16. MODEL EVALUATION
# =========================================================

accuracy = accuracy_score(
    y_test,
    predicted
)

print("\n==========================================")
print("MODEL PERFORMANCE")
print("==========================================")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predicted,
        target_names=["DOWN", "UP"],
        zero_division=0
    )
)


# =========================================================
# 17. CONFUSION MATRIX
# =========================================================

cm = confusion_matrix(
    y_test,
    predicted
)

print("Confusion Matrix:")
print(cm)


# =========================================================
# 18. FEATURE IMPORTANCE
# =========================================================

importance = pd.DataFrame(
    {
        "Feature": features,
        "Importance": model.feature_importances_
    }
)

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print("\n==========================================")
print("FEATURE IMPORTANCE")
print("==========================================")

print(
    importance.to_string(index=False)
)


# =========================================================
# 19. LATEST PREDICTION
# =========================================================

latest = latest_data[features].iloc[[-1]]

prediction = model.predict(
    latest
)[0]

probabilities = model.predict_proba(
    latest
)[0]

labels = {
    0: "DOWN",
    1: "UP"
}

direction = labels[prediction]

confidence = probabilities[prediction]


print("\n==========================================")
print("LATEST TCS PREDICTION")
print("==========================================")

print(
    "Predicted Direction:",
    direction
)

print(
    f"Confidence: {confidence * 100:.2f}%"
)

print(
    f"DOWN Probability: {probabilities[0] * 100:.2f}%"
)

print(
    f"UP Probability: {probabilities[1] * 100:.2f}%"
)

print("==========================================")


# =========================================================
# 20. SAVE LATEST PREDICTION
# =========================================================

latest_prediction = {
    "model": "Random Forest Direction Model V2",
    "prediction_date": str(
        latest_data.index[-1].date()
    ),
    "direction": direction,
    "confidence": round(
        float(confidence),
        4
    ),
    "down_probability": round(
        float(probabilities[0]),
        4
    ),
    "up_probability": round(
        float(probabilities[1]),
        4
    ),
    "validation_accuracy": round(
        float(accuracy),
        4
    )
}

with open(
    "data/direction_latest_prediction.json",
    "w"
) as file:
    json.dump(
        latest_prediction,
        file,
        indent=4
    )

print(
    "\nLatest direction prediction saved to:"
)

print(
    "data/direction_latest_prediction.json"
)
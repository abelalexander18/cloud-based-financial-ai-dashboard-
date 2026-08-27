import pandas as pd
import numpy as np
import yfinance as yf

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# =========================================================
# 1. DOWNLOAD TCS DATA
# =========================================================

ticker = "TCS.NS"

data = yf.download(
    ticker,
    start="2020-01-01",
    end="2026-08-18",
    auto_adjust=False
)

# Keep required columns
data = data[["Close", "Volume"]].copy()

# Handle yfinance MultiIndex
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data.dropna(inplace=True)


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
    data["Close"].shift(-1) /
    data["Close"] - 1
)


# =========================================================
# 9. CREATE 3-CLASS TARGET
# =========================================================

# Threshold = 0.3%
#
# Future return > +0.3%  -> UP
# Future return < -0.3%  -> DOWN
# Otherwise              -> NEUTRAL

threshold = 0.003

data["Target"] = 1

data.loc[
    data["Future_Return"] > threshold,
    "Target"
] = 2

data.loc[
    data["Future_Return"] < -threshold,
    "Target"
] = 0


# 0 = DOWN
# 1 = NEUTRAL
# 2 = UP


# =========================================================
# 10. CLEAN DATA
# =========================================================

data.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)

data.dropna(inplace=True)


# =========================================================
# 11. FEATURES
# =========================================================

features = [
    "Close",
    "Volume",
    "Daily_Return",
    "Return_5D",
    "Return_20D",
    "MA_7",
    "MA_30",
    "EMA_12",
    "EMA_26",
    "MACD",
    "MACD_Signal",
    "MACD_Histogram",
    "RSI",
    "BB_Middle",
    "BB_Upper",
    "BB_Lower",
    "BB_Position",
    "Volatility_7",
    "Volatility_20",
    "Volume_MA_20",
    "Relative_Volume"
]

X = data[features]

y = data["Target"]


# =========================================================
# 12. CHRONOLOGICAL TRAIN / TEST SPLIT
# =========================================================

split_index = int(len(data) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print("\n==========================================")
print("TCS DIRECTION MODEL V2")
print("==========================================")

print("Total observations:", len(data))
print("Training observations:", len(X_train))
print("Testing observations:", len(X_test))


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
            1: "NEUTRAL",
            2: "UP"
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
    class_weight="balanced"
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
        target_names=[
            "DOWN",
            "NEUTRAL",
            "UP"
        ],
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

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print("\n==========================================")
print("FEATURE IMPORTANCE")
print("==========================================")

print(
    importance.to_string(
        index=False
    )
)


# =========================================================
# 19. LATEST PREDICTION
# =========================================================

latest = X.iloc[[-1]]

prediction = model.predict(
    latest
)[0]

probabilities = model.predict_proba(
    latest
)[0]

labels = {
    0: "DOWN",
    1: "NEUTRAL",
    2: "UP"
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
    f"NEUTRAL Probability: {probabilities[1] * 100:.2f}%"
)

print(
    f"UP Probability: {probabilities[2] * 100:.2f}%"
)

print("==========================================")
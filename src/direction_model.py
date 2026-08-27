import pandas as pd
import numpy as np
import yfinance as yf

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ==========================================
# 1. DOWNLOAD DATA
# ==========================================

ticker = "TCS.NS"

data = yf.download(
    ticker,
    start="2020-01-01",
    end="2026-08-18",
    auto_adjust=False
)

data = data[["Close", "Volume"]].copy()

# Handle yfinance MultiIndex
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data.dropna(inplace=True)


# ==========================================
# 2. FEATURE ENGINEERING
# ==========================================

data["Daily_Return"] = data["Close"].pct_change()

data["MA_7"] = data["Close"].rolling(7).mean()

data["MA_30"] = data["Close"].rolling(30).mean()

data["Volatility_7"] = (
    data["Daily_Return"].rolling(7).std()
)

data["Previous_Close"] = (
    data["Close"].shift(1)
)

data["Previous_Return"] = (
    data["Daily_Return"].shift(1)
)

data["Momentum_7"] = (
    (data["Close"] - data["Close"].shift(7))
    / data["Close"].shift(7)
)

data["Volume_Change"] = (
    data["Volume"].pct_change()
)


# ==========================================
# 3. CREATE UP/DOWN TARGET
# ==========================================

# Tomorrow's price
data["Tomorrow_Close"] = (
    data["Close"].shift(-1)
)

# 1 = UP
# 0 = DOWN

data["Target"] = (
    data["Tomorrow_Close"] > data["Close"]
).astype(int)


# ==========================================
# 4. CLEAN DATA
# ==========================================

data.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)

data.dropna(inplace=True)


# ==========================================
# 5. FEATURES
# ==========================================

features = [
    "Close",
    "Volume",
    "Daily_Return",
    "MA_7",
    "MA_30",
    "Volatility_7",
    "Previous_Close",
    "Previous_Return",
    "Momentum_7",
    "Volume_Change"
]

X = data[features]

y = data["Target"]


# ==========================================
# 6. CHRONOLOGICAL TRAIN / TEST SPLIT
# ==========================================

split_index = int(len(data) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print("\n==========================================")
print("TCS DIRECTION PREDICTION")
print("==========================================")

print("Total observations:", len(data))
print("Training observations:", len(X_train))
print("Testing observations:", len(X_test))


# ==========================================
# 7. TRAIN RANDOM FOREST CLASSIFIER
# ==========================================

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_leaf=4,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# ==========================================
# 8. PREDICTIONS
# ==========================================

predicted = model.predict(X_test)

probabilities = model.predict_proba(X_test)

up_probability = probabilities[:, 1]


# ==========================================
# 9. EVALUATION
# ==========================================

accuracy = accuracy_score(
    y_test,
    predicted
)

precision = precision_score(
    y_test,
    predicted,
    zero_division=0
)

recall = recall_score(
    y_test,
    predicted,
    zero_division=0
)

f1 = f1_score(
    y_test,
    predicted,
    zero_division=0
)


print("\n==========================================")
print("MODEL PERFORMANCE")
print("==========================================")

print(f"Accuracy  : {accuracy * 100:.2f}%")
print(f"Precision : {precision * 100:.2f}%")
print(f"Recall    : {recall * 100:.2f}%")
print(f"F1 Score  : {f1 * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predicted,
        target_names=["DOWN", "UP"],
        zero_division=0
    )
)


# ==========================================
# 10. CONFUSION MATRIX
# ==========================================

cm = confusion_matrix(
    y_test,
    predicted
)

print("Confusion Matrix:")
print(cm)


# ==========================================
# 11. FEATURE IMPORTANCE
# ==========================================

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print("\nFeature Importance:")

print(
    importance.to_string(
        index=False
    )
)


# ==========================================
# 12. LATEST PREDICTION
# ==========================================

latest_data = X.iloc[[-1]]

latest_prediction = model.predict(
    latest_data
)[0]

latest_probability = model.predict_proba(
    latest_data
)[0]

if latest_prediction == 1:
    direction = "UP"
    confidence = latest_probability[1]
else:
    direction = "DOWN"
    confidence = latest_probability[0]


print("\n==========================================")
print("LATEST TCS PREDICTION")
print("==========================================")

print("Predicted Direction:", direction)

print(
    f"Confidence: {confidence * 100:.2f}%"
)

print(
    f"UP Probability: {latest_probability[1] * 100:.2f}%"
)

print(
    f"DOWN Probability: {latest_probability[0] * 100:.2f}%"
)

print("==========================================")
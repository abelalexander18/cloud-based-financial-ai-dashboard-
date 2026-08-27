import pandas as pd
import numpy as np
import yfinance as yf

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ==========================================
# 1. DOWNLOAD TCS DATA
# ==========================================

ticker = "TCS.NS"

data = yf.download(
    ticker,
    start="2020-01-01",
    end="2026-08-18",
    auto_adjust=False
)

# Keep only required columns
data = data[["Close", "Volume"]].copy()

# Flatten yfinance multi-level columns
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

# Previous day's price
data["Previous_Close"] = data["Close"].shift(1)

# Previous day's return
data["Previous_Return"] = data["Daily_Return"].shift(1)

# Price momentum
data["Momentum_7"] = (
    data["Close"] - data["Close"].shift(7)
) / data["Close"].shift(7)

# Volume change
data["Volume_Change"] = data["Volume"].pct_change()


# ==========================================
# 3. TARGET
# ==========================================

# Tomorrow's return
data["Target_Return"] = (
    data["Close"].shift(-1) / data["Close"] - 1
)


# Remove missing values
# Replace infinity values with NaN
data.replace([np.inf, -np.inf], np.nan, inplace=True)

# Remove rows containing missing or invalid values
data.dropna(inplace=True)


# ==========================================
# 4. FEATURES
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

y = data["Target_Return"]


# ==========================================
# 5. CHRONOLOGICAL TRAIN / TEST SPLIT
# ==========================================

split_index = int(len(data) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

data_test = data.iloc[split_index:].copy()


print("\n==========================================")
print("RANDOM FOREST FORECASTING")
print("==========================================")

print("Total observations:", len(data))

print("Training observations:", len(X_train))

print("Testing observations:", len(X_test))


# ==========================================
# 6. TRAIN RANDOM FOREST
# ==========================================

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# ==========================================
# 7. PREDICT NEXT-DAY RETURN
# ==========================================

predicted_return = model.predict(X_test)


# ==========================================
# 8. CONVERT RETURN TO PRICE
# ==========================================

current_price = data_test["Close"].values

predicted_price = (
    current_price * (1 + predicted_return)
)

actual_price = (
    data_test["Close"].shift(-1).values
)

# Last value has no next-day actual price
valid = ~np.isnan(actual_price)

actual_price = actual_price[valid]

predicted_price = predicted_price[valid]

dates = data_test.index[valid]


# ==========================================
# 9. EVALUATION
# ==========================================

# Random Forest metrics
rf_mae = mean_absolute_error(
    actual_price,
    predicted_price
)

rf_rmse = np.sqrt(
    mean_squared_error(
        actual_price,
        predicted_price
    )
)

rf_mape = np.mean(
    np.abs(
        (actual_price - predicted_price)
        / actual_price
    )
) * 100


# ==========================================
# 10. NAIVE BASELINE
# ==========================================

# Simple assumption:
# Tomorrow's price = today's price

baseline_price = current_price[valid]

baseline_mae = mean_absolute_error(
    actual_price,
    baseline_price
)

baseline_rmse = np.sqrt(
    mean_squared_error(
        actual_price,
        baseline_price
    )
)

baseline_mape = np.mean(
    np.abs(
        (actual_price - baseline_price)
        / actual_price
    )
) * 100


# ==========================================
# 11. DIRECTIONAL ACCURACY
# ==========================================

actual_direction = np.sign(
    actual_price - current_price[valid]
)

predicted_direction = np.sign(
    predicted_price - current_price[valid]
)

directional_accuracy = np.mean(
    actual_direction == predicted_direction
) * 100


# ==========================================
# 12. DISPLAY RESULTS
# ==========================================

print("\n==========================================")
print("MODEL VALIDATION")
print("==========================================")

print("\nRandom Forest:")
print(f"MAE  : ₹{rf_mae:.2f}")
print(f"RMSE : ₹{rf_rmse:.2f}")
print(f"MAPE : {rf_mape:.2f}%")

print("\nNaive Baseline:")
print(f"MAE  : ₹{baseline_mae:.2f}")
print(f"RMSE : ₹{baseline_rmse:.2f}")
print(f"MAPE : {baseline_mape:.2f}%")

print("\nDirectional Accuracy:")
print(f"{directional_accuracy:.2f}%")

print("\n==========================================")


# ==========================================
# 13. PLOT RECENT TEST RESULTS
# ==========================================

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.plot(
    dates,
    actual_price,
    label="Actual Price"
)

plt.plot(
    dates,
    predicted_price,
    label="Random Forest"
)

plt.plot(
    dates,
    baseline_price,
    label="Naive Baseline",
    linestyle="--"
)

plt.title(
    "TCS Next-Day Price Prediction - Model Validation"
)

plt.xlabel("Date")
plt.ylabel("Price (INR)")

plt.legend()
plt.grid()

plt.tight_layout()

plt.show()
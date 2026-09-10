import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ==========================================
# 1. LOAD PROCESSED TCS DATA
# ==========================================

data = pd.read_csv(
    "data/processed_market_data.csv"
)

data["Date"] = pd.to_datetime(data["Date"])
data.set_index("Date", inplace=True)

data = data[["Close", "Volume"]].copy()
data.dropna(inplace=True)

print("Loaded processed market data successfully.")
print("Observations:", len(data))


# ==========================================
# 2. FEATURE ENGINEERING
# ==========================================

data["Daily_Return"] = data["Close"].pct_change()

data["MA_7"] = (
    data["Close"].rolling(7).mean()
)

data["MA_30"] = (
    data["Close"].rolling(30).mean()
)

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
# 3. TARGET
# ==========================================

data.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)

data["Target_Return"] = (
    data["Close"].shift(-1)
    / data["Close"]
    - 1
)


# ==========================================
# 3A. CREATE TRAINING DATA
# ==========================================

# The latest row has no known next-day return,
# so it cannot be used for training.

training_data = data.dropna(
    subset=["Target_Return"]
).copy()


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

X = training_data[features]
y = training_data["Target_Return"]


# ==========================================
# 5. CHRONOLOGICAL TRAIN / TEST SPLIT
# ==========================================

split_index = int(len(X) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

data_test = training_data.iloc[split_index:].copy()

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

rf_mape = (
    np.mean(
        np.abs(
            (actual_price - predicted_price)
            / actual_price
        )
    )
    * 100
)


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

baseline_mape = (
    np.mean(
        np.abs(
            (actual_price - baseline_price)
            / actual_price
        )
    )
    * 100
)


# ==========================================
# 11. DIRECTIONAL ACCURACY
# ==========================================

actual_direction = np.sign(
    actual_price - current_price[valid]
)

predicted_direction = np.sign(
    predicted_price - current_price[valid]
)

directional_accuracy = (
    np.mean(
        actual_direction == predicted_direction
    )
    * 100
)


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
# 13. PLOT ACTUAL VS PREDICTED
# ==========================================

os.makedirs(
    "data/graphs",
    exist_ok=True
)

plt.figure(figsize=(14, 7))

plt.plot(
    dates,
    actual_price,
    label="Actual Price"
)

plt.plot(
    dates,
    predicted_price,
    label="Random Forest Predicted Price"
)

plt.plot(
    dates,
    baseline_price,
    label="Naive Baseline",
    linestyle="--"
)

plt.title(
    "TCS Next-Day Price Prediction - Random Forest Validation"
)

plt.xlabel("Date")
plt.ylabel("Stock Price (₹)")

plt.legend()
plt.grid(True)
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "data/graphs/random_forest_actual_vs_predicted.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nGraph saved to:")
print(
    "data/graphs/random_forest_actual_vs_predicted.png"
)


# ==========================================
# 14. GENERATE LATEST NEXT-DAY PREDICTION
# ==========================================

# Train the final model using all rows
# for which the next-day return is known.

final_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)

final_model.fit(X, y)


# Prepare the latest market row separately.
# The latest row has no known next-day return,
# so it was excluded from training.

latest_date = data.index[-1]
latest_price = data["Close"].iloc[-1]

latest_row = data.iloc[[-1]].copy()

latest_features = latest_row[features]


# Predict next-day return

latest_predicted_return = final_model.predict(
    latest_features
)[0]


# Convert return to predicted price

latest_predicted_price = (
    latest_price
    * (1 + latest_predicted_return)
)


# ==========================================
# 15. SAVE LATEST PREDICTION
# ==========================================

latest_prediction = {
    "model": "Random Forest",
    "prediction_date": str(
        latest_date.date()
    ),
    "latest_price": round(
        float(latest_price),
        2
    ),
    "predicted_return": round(
        float(latest_predicted_return),
        6
    ),
    "predicted_next_day_price": round(
        float(latest_predicted_price),
        2
    ),
    "validation_mape": round(
        float(rf_mape),
        2
    )
}

with open(
    "data/random_forest_latest_prediction.json",
    "w"
) as file:
    json.dump(
        latest_prediction,
        file,
        indent=4
    )


# ==========================================
# 16. DISPLAY LATEST PREDICTION
# ==========================================

print("\n==========================================")
print("LATEST RANDOM FOREST PREDICTION")
print("==========================================")

print(
    f"Latest Date: {latest_date.date()}"
)

print(
    f"Latest Price: ₹{latest_price:.2f}"
)

print(
    f"Predicted Return: "
    f"{latest_predicted_return:.4%}"
)

print(
    f"Predicted Next-Day Price: "
    f"₹{latest_predicted_price:.2f}"
)

print("\nSaved to:")
print(
    "data/random_forest_latest_prediction.json"
)

print("==========================================")
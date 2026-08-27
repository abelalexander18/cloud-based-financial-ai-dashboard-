import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import os


# ==========================================
# 1. DOWNLOAD STOCK DATA
# ==========================================
ticker = "TCS.NS"

data = yf.download(
    ticker,
    start="2020-01-01",
    end="2026-08-18",
    auto_adjust=False
)


# ==========================================
# 2. PREPARE DATA
# ==========================================
forecast_data = data[["Close"]].copy()

# Handle yfinance MultiIndex
if isinstance(forecast_data.columns, pd.MultiIndex):
    forecast_data.columns = forecast_data.columns.get_level_values(0)

forecast_data = forecast_data.reset_index()

forecast_data.columns = ["ds", "y"]

forecast_data.dropna(inplace=True)

print("\nTotal observations:", len(forecast_data))


# ==========================================
# 3. TRAIN / TEST SPLIT
# ==========================================
split_index = int(len(forecast_data) * 0.80)

train = forecast_data.iloc[:split_index].copy()
test = forecast_data.iloc[split_index:].copy()

print("Training observations:", len(train))
print("Testing observations:", len(test))

print("\nTraining period:")
print(train["ds"].min(), "to", train["ds"].max())

print("\nTesting period:")
print(test["ds"].min(), "to", test["ds"].max())


# ==========================================
# 4. TRAIN PROPHET MODEL
# ==========================================
model = Prophet()

model.fit(train)


# ==========================================
# 5. PREDICT TEST PERIOD
# ==========================================
future = test[["ds"]].copy()

forecast = model.predict(future)


# ==========================================
# 6. GET ACTUAL AND PREDICTED VALUES
# ==========================================
actual = test["y"].values

predicted = forecast["yhat"].values


# ==========================================
# 7. CALCULATE EVALUATION METRICS
# ==========================================
mae = mean_absolute_error(
    actual,
    predicted
)

rmse = np.sqrt(
    mean_squared_error(
        actual,
        predicted
    )
)

mape = np.mean(
    np.abs(
        (actual - predicted) / actual
    )
) * 100


# ==========================================
# 8. DISPLAY RESULTS
# ==========================================
print("\n")
print("=" * 50)
print("       PROPHET MODEL PERFORMANCE")
print("=" * 50)

print(f"MAE  : ₹{mae:.2f}")
print(f"RMSE : ₹{rmse:.2f}")
print(f"MAPE : {mape:.2f}%")

print("=" * 50)


# ==========================================
# 9. ACTUAL VS PREDICTED DATA
# ==========================================
results = pd.DataFrame({
    "Date": test["ds"],
    "Actual": actual,
    "Predicted": predicted
})

print("\nActual vs Predicted:")
print(results.head(10))


# ==========================================
# 10. SAVE RESULTS
# ==========================================
os.makedirs(
    "data/graphs",
    exist_ok=True
)

results.to_csv(
    "data/tcs_forecast_evaluation.csv",
    index=False
)


# ==========================================
# 11. PLOT ACTUAL VS PREDICTED
# ==========================================

plt.figure(figsize=(14, 7))

plt.plot(
    results["Date"],
    results["Actual"],
    label="Actual Values"
)

plt.plot(
    results["Date"],
    results["Predicted"],
    label="Predicted Values"
)

plt.title(
    "TCS Stock Price - Actual vs Predicted"
)

plt.xlabel("Date")

plt.ylabel(
    "Stock Price (₹)"
)

plt.legend()

plt.grid(True)

plt.xticks(rotation=45)

plt.tight_layout()


# Save graph
plt.savefig(
    "data/graphs/tcs_actual_vs_predicted.png",
    dpi=300,
    bbox_inches="tight"
)


# Display graph
plt.show()

plt.close()


print(
    "\nGraph saved to:"
)

print(
    "data/graphs/tcs_actual_vs_predicted.png"
)
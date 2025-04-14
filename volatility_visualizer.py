import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf


# Function to calculate historical volatility
def calculate_volatility(data, window=252):
    log_returns = np.log(data / data.shift(1))
    volatility = log_returns.rolling(window=window).std() * np.sqrt(window)
    return volatility


# Fetch historical data for multiple assets
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
data = yf.download(tickers, start="2020-01-01", end="2025-01-01")

close_price = data["Close"]

# Calculate volatility for each asset
volatility_data = pd.DataFrame()
for ticker in tickers:
    volatility_data[ticker] = calculate_volatility(close_price[ticker])

# Plot the volatility
plt.figure(figsize=(14, 7))
for ticker in tickers:
    plt.plot(volatility_data[ticker], label=ticker)
plt.title("Historical Volatility")
plt.xlabel("Date")
plt.ylabel("Volatility")
plt.legend()
plt.show()

# Heatmap of volatilities
sns.heatmap(volatility_data.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation of Volatilities")
plt.show()

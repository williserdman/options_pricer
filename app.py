import streamlit as st
from black_scholes_function import black_scholes

st.set_page_config(layout="wide")


@st.cache_data
def bs_cached(s, k, t, r, o, type):
    return black_scholes(s, k, t, r, o, type)


st.sidebar.title("Simple Put/Call Calculator")

### Sidebar ###

with st.sidebar.form(key="scholes_input_form", clear_on_submit=False):
    current_price = st.number_input("Current Stock Price", value=31.55)
    strike_price = st.number_input("Strike Price", value=22.75)
    time_to_expiration = st.number_input("Time to Expiration (years)", value=3.5)
    risk_free_rate = st.number_input("Risk Free Rate (%)", value=5)
    volatility = st.number_input("Volatility (%)", value=50)
    # type = st.selectbox("type", ["call", "put"])

    st.form_submit_button()

columns = st.sidebar.columns(2)

with columns[0]:
    st.header("PUT")
    st.write(
        bs_cached(
            current_price,
            strike_price,
            time_to_expiration,
            risk_free_rate,
            volatility,
            "put",
        )
    )
with columns[1]:
    st.header("CALL")
    st.write(
        bs_cached(
            current_price,
            strike_price,
            time_to_expiration,
            risk_free_rate,
            volatility,
            "call",
        )
    )

### end Sidebar ###

### Main Columns ###

outer_columns = st.columns(2)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

with outer_columns[0]:
    st.title("Black-Scholes Option Pricing Sensitivity Analysis")

    # Dropdowns for selecting parameters
    params = [
        "Current Stock Price",
        "Strike Price",
        "Time to Expiration (years)",
        "Risk Free Rate (%)",
        "Volatility (%)",
    ]
    y_param = st.selectbox("Select X-axis Parameter", params, index=2)
    x_param = st.selectbox("Select Y-axis Parameter", params, index=3)
    c_inner = st.columns(2)

    with c_inner[0]:
        option_type = st.selectbox("Select Option Type", ["call", "put"])
    with c_inner[1]:
        precision = st.slider("Precision", 10, 50, 20)

    # Define ranges for parameters
    param_ranges = {
        "Current Stock Price": np.linspace(
            current_price - current_price * 0.3,
            current_price + current_price * 0.3,
            precision,
        ),
        "Strike Price": np.linspace(
            strike_price - strike_price * 0.3,
            strike_price + strike_price * 0.3,
            precision,
        ),
        "Time to Expiration (years)": np.linspace(0.1, 4, precision),
        "Risk Free Rate (%)": np.linspace(1, 10, precision),
        "Volatility (%)": np.linspace(1, 100, precision),
    }

    # Generate data for heatmap
    x_values = param_ranges[x_param][
        ::-1
    ]  # to count backwards, this puts (min, min) in bottom left instead of top left
    y_values = param_ranges[y_param]

    prices = np.zeros((len(x_values), len(y_values)))
    # print(prices)

    for i, x in enumerate(y_values):
        for j, y in enumerate(x_values):
            params_dict = {
                params[0]: current_price,
                params[1]: strike_price,
                params[2]: time_to_expiration,
                params[3]: risk_free_rate,
                params[4]: volatility,
            }
            params_dict[x_param] = x
            params_dict[y_param] = y
            print(params_dict)
            prices[i, j] = bs_cached(
                params_dict[params[0]],
                params_dict[params[1]],
                params_dict[params[2]],
                params_dict[params[3]],
                params_dict[params[4]],
                option_type,
            )
            print(prices)

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        prices,
        xticklabels=np.round(y_values, 2),
        yticklabels=np.round(x_values, 2),
        cmap="coolwarm",
        ax=ax,
    )
    ax.set_xlabel(y_param)
    ax.set_ylabel(x_param)
    ax.set_title(f"{option_type.capitalize()} Option Price Sensitivity Analysis")
    st.pyplot(fig)


with outer_columns[1]:

    st.title("Volatility and Time-Sensitivity Analysis")

    with st.form(key="volatility_ticker_list", clear_on_submit=False):
        text_input = st.text_input(
            "Enter values separated by commas:",
            value="SPY, AAPL, MSFT, GOOGL, AMZN, TSLA",
        )

        if text_input:
            tickers = [item.strip() for item in text_input.split(",")]
            # st.write("List of strings:", string_list)
        else:
            tickers = ["SPY", "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

        st.form_submit_button()

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
    data = yf.download(tickers, start="2020-01-01", end="2025-01-01")

    close_price = data["Close"]

    # Calculate volatility for each asset
    volatility_data = pd.DataFrame()
    for ticker in tickers:
        volatility_data[ticker] = calculate_volatility(close_price[ticker])

    # Plot the volatility
    vol_graph = plt.figure(figsize=(14, 7))
    for ticker in tickers:
        plt.plot(volatility_data[ticker], label=ticker)
    plt.title("Historical Volatility")
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.legend()
    st.pyplot(vol_graph)
    # Heatmap of volatilities
    vol_map = plt.figure()
    sns.heatmap(volatility_data.corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation of Volatilities")
    # st.pyplot(heatmap)
    st.pyplot(vol_map)

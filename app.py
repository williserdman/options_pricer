import streamlit as st
from black_scholes_function import black_scholes

st.title("Simple Black-Scholes Calculator")


@st.cache_data
def bs_cached(s, k, t, r, o, type):
    return black_scholes(s, k, t, r, o, type)


with st.form(key="scholes_input_form", clear_on_submit=False):
    current_price = st.number_input("current stock price", value=1000)
    strike_price = st.number_input("strike price", value=1050)
    time_to_expiration = st.number_input("time to expiration (years)", value=0.5)
    risk_free_rate = st.number_input("risk free rate", value=0.5)
    volatility = st.number_input("volatility", value=0.5)
    # type = st.selectbox("type", ["call", "put"])

    st.form_submit_button()


columns = st.columns(2)

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

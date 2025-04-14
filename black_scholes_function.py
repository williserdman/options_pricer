import numpy as np
from scipy.stats import norm


def black_scholes(S, K, T, r, sigma, option_type="call"):
    """
    Vectorized Black-Scholes pricing for European options.
    Handles scalars, arrays, or matrices of inputs.

    Parameters:
        S (float/array): Current stock price(s)
        K (float/array): Strike price(s)
        T (float/array): Time to expiration (years)
        r (float/array): Risk-free rate(s)
        sigma (float/array): Volatility (\sigma) # how to do latex in StreamLit
        option_type (str): 'call' or 'put'

    Returns:
        float/array: Option price(s)
    """
    # Ensure inputs are numpy arrays for vectorization
    S = np.asarray(S)
    K = np.asarray(K)
    T = np.asarray(T)
    r = np.asarray(r) / 100
    sigma = np.asarray(sigma) / 100

    # Compute d1 and d2 (element-wise)
    # print(np.log(S / K))
    # print((r + 0.5 * sigma**2) * T)

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Compute option prices

    if option_type == "call":
        norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        # print((S * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2)))
        # print(price)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return price


if __name__ == "__main__":
    print(black_scholes(31.55, 22.75, 3.5, 5, 50))

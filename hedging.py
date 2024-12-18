#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from scipy.optimize import bisect
from scipy.stats import norm


# In[ ]:


# Load the data file
file_path = '/mnt/data/Option_SPX.csv'
data = pd.read_csv(file_path)

# Black-Scholes call option pricing formula
def black_scholes_call_price(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Function to calculate implied volatility
def implied_volatility(C_mkt, S, K, T, r):
    def objective(sigma):
        return black_scholes_call_price(S, K, T, r, sigma) - C_mkt
    try:
        return bisect(objective, 1e-6, 5)  # Searching for sigma in a reasonable range
    except ValueError:
        return np.nan

# Function to calculate Delta using the Black-Scholes model
def black_scholes_delta(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# Crank-Nicholson method for solving the Black-Scholes PDE
def crank_nicholson(S, K, r, T, sigma, N=100, M=100):
    dt = T / N  # Time step size
    dx = sigma * np.sqrt(3 * dt)  # Price step size
    pu = 0.5 * dt * ((sigma / dx)**2 + (r - 0.5 * sigma**2) / dx)
    pm = 1 - dt * (sigma / dx)**2 - r * dt
    pd = 0.5 * dt * ((sigma / dx)**2 - (r - 0.5 * sigma**2) / dx)

    # Initialize the price grid
    S_grid = S * np.exp(dx * (np.arange(-M, M+1)))
    V = np.maximum(S_grid - K, 0)  # Option value at maturity

    # Backward iteration to solve the PDE
    for _ in range(N):
        V[1:-1] = pu * V[:-2] + pm * V[1:-1] + pd * V[2:]
        V[0] = 0  # Boundary condition at S = 0
        V[-1] = S_grid[-1] - K  # Boundary condition at S -> infinity
    return V[M]

# Initialize strategy variables
position = 0  # Current asset position
cash = 0      # Cash balance
portfolio_values = []  # Store portfolio values over time
predicted_prices = []  # Store predicted option prices

# Iterate over each row of the data to implement the hedging strategy
for i in range(len(data)):
    S = data['S'][i]  # Current stock price
    K = S * np.exp(-data['Moneyness'][i] / 100)  # Calculate strike price based on Moneyness
    T = data['TTM'][i] / 252  # Convert time to expiration to years
    r = data['R'][i] / 100  # Convert interest rate to decimal
    C_mkt = data['C_mkt'][i]  # Market option price

    # Calculate implied volatility
    sigma = implied_volatility(C_mkt, S, K, T, r)

    # Skip this row if implied volatility could not be calculated
    if np.isnan(sigma):
        continue

    # Calculate Delta using Crank-Nicholson if needed
    V_up = crank_nicholson(S * 1.01, K, r, T, sigma)
    V_down = crank_nicholson(S * 0.99, K, r, T, sigma)
    delta = (V_up - V_down) / (S * 0.02)

    # Calculate predicted option price using Crank-Nicholson
    predicted_price = crank_nicholson(S, K, r, T, sigma)
    predicted_prices.append(predicted_price)

    # Determine the target position based on Delta
    target_position = -delta
    position_change = target_position - position

    # Update cash and asset position
    cash -= position_change * S
    position = target_position

    # Record portfolio value
    portfolio_values.append(position * S + cash)

# Convert portfolio values to a DataFrame for further analysis
portfolio_values = pd.DataFrame(portfolio_values, columns=['Portfolio Value'])

# Print predicted prices
predicted_prices_df = pd.DataFrame(predicted_prices, columns=['Predicted Price'])
print(predicted_prices_df)

# Calculate risk metrics
portfolio_values['Returns'] = portfolio_values['Portfolio Value'].pct_change().dropna()
volatility = portfolio_values['Returns'].std()  # Calculate return volatility
cumulative_returns = (1 + portfolio_values['Returns']).cumprod()
drawdown = cumulative_returns.cummax() - cumulative_returns  # Calculate drawdown
max_drawdown = drawdown.max()

# Output risk metrics
volatility, max_drawdown


# In[ ]:





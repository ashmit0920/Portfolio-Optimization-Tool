"""## Data collection, risk and return calculation"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.optimize import minimize
import cvxpy as cp

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
data = yf.download(tickers, start='2020-01-01', end='2024-01-01')['Adj Close']

# Calculate daily returns
returns = data.pct_change().dropna()

# Expected returns (mean of daily returns)
mean_returns = returns.mean()

# Covariance matrix of returns
cov_matrix = returns.cov()

"""## Optimization function"""

def portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate=0.01):
    returns = np.dot(weights, mean_returns)
    std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = (returns - risk_free_rate) / std_dev
    return std_dev, returns, sharpe_ratio

def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0.01):
    return -portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate)[2]

def optimize_portfolio(mean_returns, cov_matrix, risk_free_rate=0.01, min_weight=0.05, max_weight=0.35):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate)

    # Adding weight constraints
    bounds = tuple((min_weight, max_weight) for _ in range(num_assets))
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    # Optimizing for maximum Sharpe ratio
    result = minimize(neg_sharpe_ratio, num_assets * [1. / num_assets,], args=args,
                      method='SLSQP', bounds=bounds, constraints=constraints)
    return result

"""## Running the optimization"""

optimal_portfolio = optimize_portfolio(mean_returns, cov_matrix)
optimal_weights = optimal_portfolio.x

std_dev, returns, sharpe_ratio = portfolio_performance(optimal_weights, mean_returns, cov_matrix)

print("Optimal Weights: ", optimal_weights)
print("Expected Return: ", returns)
print("Expected Volatility: ", std_dev)
print("Sharpe Ratio: ", sharpe_ratio)

"""## Visualization"""

def plot_efficient_frontier(mean_returns, cov_matrix, risk_free_rate=0.01, num_portfolios=10000):
    results = np.zeros((3, num_portfolios))
    weights_record = []
    num_assets = len(mean_returns)

    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)
        portfolio_std_dev, portfolio_return, _ = portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate)
        results[0,i] = portfolio_std_dev
        results[1,i] = portfolio_return
        results[2,i] = (portfolio_return - risk_free_rate) / portfolio_std_dev

    max_sharpe_idx = np.argmax(results[2])
    sdp, rp = results[0, max_sharpe_idx], results[1, max_sharpe_idx]
    max_sharpe_allocation = weights_record[max_sharpe_idx]

    trace1 = go.Scatter(
        x=results[0,:],
        y=results[1,:],
        mode='markers',
        marker=dict(color=results[2,:], colorscale='Viridis', showscale=True),
        text=weights_record
    )
    trace2 = go.Scatter(
        x=[sdp],
        y=[rp],
        mode='markers',
        marker=dict(color='red', size=14, symbol='x'),
        name='Maximum Sharpe ratio'
    )

    data = [trace1, trace2]

    layout = go.Layout(
        title='Efficient Frontier',
        xaxis=dict(title='Volatility'),
        yaxis=dict(title='Return'),
        showlegend=True
    )

    fig = go.Figure(data=data, layout=layout)
    return fig


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Portfolio Optimization Tool", className='text-center'), className="mb-4 mt-4")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Enter Ticker Symbols (comma separated)"),
                    dbc.Input(id='tickers', placeholder="AAPL, MSFT, GOOGL, AMZN, FB", type="text")
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Start Date"),
                    dbc.Input(id='start-date', placeholder="2020-01-01", type="text")
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("End Date"),
                    dbc.Input(id='end-date', placeholder="2023-01-01", type="text")
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Risk Tolerance"),
                    dcc.Slider(
                        id='risk-tolerance',
                        min=0,
                        max=1,
                        step=0.1,
                        marks={i / 10: str(i / 10) for i in range(11)},
                        value=0.5
                    )
                ]),
            ]),
            dbc.Button("Optimize", id='optimize-button', color="primary")
        ], width=4),
        dbc.Col([
            dcc.Graph(id='efficient-frontier')
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col([
            html.H4("Optimal Weights"),
            html.Div(id='optimal-weights')
        ])
    ])
])

@app.callback(
    [Output('efficient-frontier', 'figure'),
     Output('optimal-weights', 'children')],
    [Input('optimize-button', 'n_clicks')],
    [dash.dependencies.State('tickers', 'value'),
     dash.dependencies.State('start-date', 'value'),
     dash.dependencies.State('end-date', 'value'),
     dash.dependencies.State('risk-tolerance', 'value')]
)
def update_output(n_clicks, tickers, start_date, end_date, risk_tolerance):
    if not n_clicks:
        return go.Figure(), ""

    tickers = [ticker.strip() for ticker in tickers.split(',')]
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    returns = data.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    
    # Adjust risk-free rate based on risk tolerance
    risk_free_rate = 0.01 * (1 - risk_tolerance)
    
    optimal_portfolio = optimize_portfolio(mean_returns, cov_matrix, risk_free_rate)
    optimal_weights = optimal_portfolio.x
    optimal_weights_str = ', '.join([f"{ticker}: {weight:.2%}" for ticker, weight in zip(tickers, optimal_weights)])
    
    fig = plot_efficient_frontier(mean_returns, cov_matrix, risk_free_rate)
    
    return fig, optimal_weights_str

if __name__ == '__main__':
    app.run_server(debug=True)

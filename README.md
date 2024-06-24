# Portfolio-Optimization-Tool

A portfolio optimization tool helps investors allocate their assets in a way that maximizes return for a given level of risk or minimizes risk for a given level of return. One common approach is using the Modern Portfolio Theory (MPT), developed by Harry Markowitz, which focuses on the trade-off between risk and return.

## Install Required Libraries

Setup a virtual environment to prevent dependency conflicts (highly recommended). Type the following commands in a Windows terminal inside the project directory.
```
python -m venv venv
```
```
venv\bin\activate
```
Install the required libraries.
```
pip install dash dash-bootstrap-components yfinance pandas numpy matplotlib scipy cvxpy
```

## Working 

The expected returns and covariance matrix is calculated for 5 companies, the yfinance library is used to collect the data. An optimization function is defined to maximize the Sharpe ratio. Certain constraints are added to ensure a more balanced portfolio and avoid "corner solutions", such as setting minimum and maximum weights for each asset. Another approach is to add a regularization term to the optimization objective to penalize highly concentrated portfolios. At the end, the efficient frontier is plotted for visualization purposes.

The user interface is created using **Dash**, a web framework for building analytical web applications in Python. The UI provides input fields to enter the company names (ticker symbols), start and end dates for the data to be analyzed and a Risk Tolerance slider.

To run the program, clone the repo and run the main.py file.
```
python main.py
```
Open a web browser and navigate to:
```
http://127.0.0.1:8050/
```

On clicking the "Optimize" button, a Return v/s Volatility graph is plotted and the Optimal weights and various other performance metrics are calculated and displayed. The "X" in the graph symbolizes the maximum **Sharpe Ratio**.

![UI screenshot](./User%20Interface.png)

## Run using Docker

Make sure you have Docker installed on your PC. You don't need to follow the steps mentioned above while using Docker. Clone the repo and navigate to the project directory from your terminal. Then, type -
```
docker build -t portfolio-optimizer .
```
```
docker run -p 8050:8050 portfolio-optimizer
```

Open a web browser and navigate to: ```http://127.0.0.1:8050/ ```

## Future updates

- **Enhance the Model:** Incorporate more sophisticated risk measures, such as Conditional Value at Risk (CVaR).

- **User-defined constraints:** Allow users to set specific constraints, such as minimum and maximum allocation for each asset, or constraints on sector or asset type allocations.

- **Performance Monitoring:** Set up a system to track the performance of the optimized portfolio over time and compare it with benchmarks.
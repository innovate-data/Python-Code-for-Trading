"""Compute daily returns."""

import os
import pandas as pd
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()


def compute_daily_returns(df):
    """Compute and return the daily return values."""
    
    # create a copy of data frame
    df_dr = df.copy()
    
    # find number of rows
    r = df_dr.shape[0]
    
    # calculate the daily return for rows 1:r
    df_dr.iloc[1:r] = (df_dr.iloc[1:r]/df_dr.iloc[0:r-1].values) - 1
    
    # set the daily return foe row 0 to 0
    df_dr.iloc[0]=0
    
    # replace NaN with 0
    df_dr = df_dr.fillna(0)
 
    return(df_dr)

def compute_daily_returns_using_pandas(df):
    """Compute and return the daily return values."""
    
  
    df_dr = (df/df.shift(1))  -1
    
    # replace NaN with 0
    df_dr = df_dr.fillna(0)
 
    return(df_dr)

def test_run():
    # Read data
    dates = pd.date_range('2012-07-01', '2012-07-31')  # one month only
    symbols = ['SPY','XOM']
    df = get_data(symbols, dates)
  
    plot_data(df)

    # Compute daily returns
    daily_returns = compute_daily_returns(df)
    plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")

    # Compute daily returns using pandas
    daily_returns2 = compute_daily_returns_using_pandas(df)
    plot_data(daily_returns2, title="Daily returns using Pandas", ylabel="Daily returns")


test_run()

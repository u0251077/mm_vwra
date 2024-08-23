import yfinance as yf
import streamlit as st
import pandas as pd
import altair as alt
from typing import Dict, Any

# Constants
STOCK_TICKER = "VWRA.L"
STOCK_COUNT = 12
ALREADY_INVESTED = 50000
TWD_BALANCE = 195

def get_stock_data(ticker: str) -> pd.DataFrame:
    """Download and return historical stock data."""
    stock_data = yf.download(ticker, period="max", progress=False)
    return stock_data.sort_index()

def get_stock_price(ticker: str) -> float:
    """Get the latest stock price."""
    stock = yf.Ticker(ticker)
    stock_info = stock.history(period='1d')
    return stock_info['Close'].iloc[-1]

def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """Get the latest exchange rate."""
    ticker = f'{base_currency}{target_currency}=X'
    exchange_rate = yf.Ticker(ticker).history(period='1d')
    return exchange_rate['Close'].iloc[-1]

def create_stock_chart(stock_data: pd.DataFrame) -> alt.Chart:
    """Create an Altair chart for stock data."""
    base = alt.Chart(stock_data.reset_index()).encode(x='Date:T')
    lines = base.mark_line().encode(
        y=alt.Y('Close', title='收盤價'),
        color=alt.value('blue')
    )
    return lines

def create_transaction_table() -> pd.DataFrame:
    """Create a DataFrame for transaction details."""
    data = {
        "時間": ["(2024)113/08/06"],
        "成交時間": [f"${126.46:.2f}"],
        "成交數量": [12],
        "手續費": [f"${3.79:.2f}"],
        "美金成本": [f"${1521.31:.2f}"],
        "台幣成本": [f"${49805:.2f}"],
        "匯率": [f"{32.74:.2f}"]
    }
    return pd.DataFrame(data)

def display_stock_info(stock_price: float, exchange_rate: float) -> None:
    """Display stock information."""
    st.write(f"即時{STOCK_TICKER} 的股價: ${stock_price:.2f}")
    st.write(f"即時美元對台幣匯率: {exchange_rate:.2f}")
    st.write("------------------")
    st.write(f"當前持有數量: {STOCK_COUNT}")
    stock_sum = STOCK_COUNT * stock_price * exchange_rate
    st.write("------------------")
    st.write(f"當前總股票價值: {stock_sum:.2f}")
    st.write(f"台幣餘額: {TWD_BALANCE:.2f}")
    st.write("------------------")
    st.write(f"當前總投資金額: {ALREADY_INVESTED:.2f}")
    st.write("------------------")

def main():
    st.title("即時觀測站")

    stock_data = get_stock_data(STOCK_TICKER)
    chart = create_stock_chart(stock_data)
    st.altair_chart(chart, use_container_width=True)

    stock_price = get_stock_price(STOCK_TICKER)
    exchange_rate = get_exchange_rate('USD', 'TWD')

    display_stock_info(stock_price, exchange_rate)

    transaction_table = create_transaction_table()
    st.table(transaction_table)

if __name__ == "__main__":
    main()

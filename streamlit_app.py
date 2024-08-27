import yfinance as yf
import streamlit as st
import pandas as pd
import altair as alt
from typing import Dict, Any
from datetime import datetime

# Constants
STOCK_TICKER = "VWRA.L"
STOCK_COUNT = 12
ALREADY_INVESTED = 50000
TWD_BALANCE = 195

@st.cache_data(ttl=3600)
def get_stock_data(ticker: str) -> pd.DataFrame:
    """Download and return all historical stock data."""
    stock_data = yf.download(ticker, start="2010-01-01", end=datetime.now().strftime('%Y-%m-%d'), progress=False)
    return stock_data.sort_index()

@st.cache_data
def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.history(period='1d')
        if stock_info.empty:
            st.warning(f"No data available for {ticker}.")
            return None
        return stock_info
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
        return None

@st.cache_data(ttl=300)
def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """Get the latest exchange rate."""
    ticker = f'{base_currency}{target_currency}=X'
    exchange_rate = yf.Ticker(ticker).history(period='1d')
    return exchange_rate['Close'].iloc[-1]

def create_stock_chart(stock_data: pd.DataFrame) -> alt.Chart:
    """Create an Altair chart for all historical stock data."""
    base = alt.Chart(stock_data.reset_index()).encode(
        x=alt.X('Date:T', axis=alt.Axis(format='%Y', title='年份')),
        y=alt.Y('Close:Q', axis=alt.Axis(title='收盤價')),
        tooltip=['Date:T', 'Close:Q']
    )
    
    line = base.mark_line(color='blue')
    
    return line.properties(
        width=700,
        height=400,
        title=f"{STOCK_TICKER} 歷史價格趨勢"
    ).interactive()

def create_transaction_table() -> pd.DataFrame:
    """Create a DataFrame for transaction details."""
    data = {
        "時間": ["2024/08/06"],
        "成交價格": [126.46],
        "成交數量": [12],
        "手續費": [3.79],
        "美金成本": [1521.31],
        "台幣成本": [49805],
        "匯率": [32.74]
    }
    return pd.DataFrame(data)

def calculate_performance(current_price: float, purchase_price: float) -> float:
    """Calculate the performance of the stock."""
    return ((current_price - purchase_price) / purchase_price) * 100

def display_stock_info(stock_price: float, exchange_rate: float, transaction_data: pd.DataFrame) -> None:
    """Display stock information."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if stock_price is not None:
            st.metric("即時股價", f"${stock_price:.2f}")
        else:
            st.warning("無法取得即時股價")

    with col2:
        if exchange_rate is not None:
            st.metric("即時匯率", f"{exchange_rate:.2f}")
        else:
            st.warning("無法取得即時匯率")

    with col3:
        if stock_price is not None and not transaction_data.empty:
            if '成交價格' in transaction_data.columns and not transaction_data['成交價格'].empty:
                initial_price = transaction_data['成交價格'].iloc[0]
                performance = calculate_performance(stock_price, initial_price)
                st.metric("績效", f"{performance:.2f}%")
            else:
                st.warning("交易資料中沒有'成交價格'欄位或資料為空.")
        else:
            st.warning("交易資料無法顯示")

    st.write("------------------")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"當前持有數量: {STOCK_COUNT}")
        st.write(f"台幣餘額: {TWD_BALANCE:.2f}")
    with col2:
        st.write(f"當前總投資金額: {ALREADY_INVESTED:.2f}")
        profit_loss = current_value - ALREADY_INVESTED
        st.write(f"盈虧: {profit_loss:.2f}")

def main():
    st.set_page_config(page_title="VWRA.L 即時觀測站", layout="wide")
    st.title("VWRA.L 即時觀測站")

    #stock_data = get_stock_data(STOCK_TICKER)
    #chart = create_stock_chart(stock_data)
    
    stock_price = get_stock_price('VWRA.L')
    exchange_rate = get_exchange_rate('USD', 'TWD')
    transaction_data = create_transaction_table()

    #st.altair_chart(chart, use_container_width=True)

    display_stock_info(stock_price, exchange_rate, transaction_data)
    
    st.write("交易明細")
    st.dataframe(transaction_data.style.format({
        '成交價格': '${:.2f}',
        '手續費': '${:.2f}',
        '美金成本': '${:.2f}',
        '台幣成本': '${:.2f}',
        '匯率': '{:.2f}'
    }))

if __name__ == "__main__":
    main()

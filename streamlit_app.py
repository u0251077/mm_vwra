import yfinance as yf
import streamlit as st
import pandas as pd
import altair as alt
from typing import Dict, Any
from datetime import datetime, timedelta

# Constants
STOCK_TICKER = "VWRA.L"
STOCK_COUNT = 12
ALREADY_INVESTED = 50000
TWD_BALANCE = 195

@st.cache_data(ttl=3600)
def get_stock_data(ticker: str) -> pd.DataFrame:
    """Download and return all historical stock data."""
    try:
        stock_data = yf.download(ticker, start="2010-01-01", end=datetime.now().strftime('%Y-%m-%d'), progress=False)
        if stock_data.empty:
            st.warning(f"无法获取 {ticker} 的历史数据。")
            return pd.DataFrame(columns=['Date', 'Close'])
        return stock_data.sort_index()
    except Exception as e:
        st.error(f"获取 {ticker} 的历史数据时出错：{str(e)}")
        return pd.DataFrame(columns=['Date', 'Close'])

@st.cache_data(ttl=300)
def get_stock_price(ticker: str) -> float:
    """Get the latest stock price."""
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.history(period='1d')
        if stock_info.empty:
            st.warning(f"无法获取 {ticker} 的最新价格。")
            return 0.0
        return stock_info['Close'].iloc[-1]
    except Exception as e:
        st.error(f"获取 {ticker} 的最新价格时出错：{str(e)}")
        return 0.0

@st.cache_data(ttl=300)
def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """Get the latest exchange rate."""
    try:
        ticker = f'{base_currency}{target_currency}=X'
        exchange_rate = yf.Ticker(ticker).history(period='1d')
        if exchange_rate.empty:
            st.warning(f"无法获取 {base_currency}/{target_currency} 的汇率。")
            return 0.0
        return exchange_rate['Close'].iloc[-1]
    except Exception as e:
        st.error(f"获取 {base_currency}/{target_currency} 汇率时出错：{str(e)}")
        return 0.0

def create_stock_chart(stock_data: pd.DataFrame) -> alt.Chart:
    """Create an Altair chart for all historical stock data."""
    if stock_data.empty:
        return alt.Chart(pd.DataFrame({'Date': [datetime.now()], 'Close': [0]})).mark_line()
    
    base = alt.Chart(stock_data.reset_index()).encode(
        x=alt.X('Date:T', axis=alt.Axis(format='%Y', title='年份')),
        y=alt.Y('Close:Q', axis=alt.Axis(title='收盘价')),
        tooltip=['Date:T', 'Close:Q']
    )
    
    line = base.mark_line(color='blue')
    
    return line.properties(
        width=700,
        height=400,
        title=f"{STOCK_TICKER} 历史价格趋势"
    ).interactive()

# ... [其余函数保持不变] ...

def main():
    st.set_page_config(page_title="VWRA.L 即时观测站", layout="wide")
    st.title("VWRA.L 即时观测站")

    stock_data = get_stock_data('VWRA.L')
    chart = create_stock_chart(stock_data)
    
    stock_price = get_stock_price('VWRA.L')
    exchange_rate = get_exchange_rate('USD', 'TWD')
    transaction_data = create_transaction_table()

    st.altair_chart(chart, use_container_width=True)

    if stock_price > 0 and exchange_rate > 0:
        display_stock_info(stock_price, exchange_rate, transaction_data)
    else:
        st.warning("无法显示股票信息，因为无法获取股价或汇率数据。")
    
    st.write("交易明细")
    st.dataframe(transaction_data.style.format({
        '成交价格': '${:.2f}',
        '手续费': '${:.2f}',
        '美金成本': '${:.2f}',
        '台币成本': '${:.2f}',
        '汇率': '{:.2f}'
    }))

if __name__ == "__main__":
    main()

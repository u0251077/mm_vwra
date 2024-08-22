import yfinance as yf
import streamlit as st
import pandas as pd
import altair as alt

def get_stock_data(ticker):
    stock_data = yf.download(ticker, period="max", progress=False)
    stock_data = stock_data.sort_index()
    return stock_data

# 獲取 VWRA.L 的股價
def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    stock_info = stock.history(period='1d')
    return stock_info['Close'].iloc[-1]


def get_exchange_rate(base_currency, target_currency):
    ticker = f'{base_currency}{target_currency}=X'
    exchange_rate = yf.Ticker(ticker).history(period='1d')
    return exchange_rate['Close'].iloc[-1]

def main():
    st.title("即時觀測")

    stock_data = get_stock_data("VWRA.L")
    # 用Altair繪製圖表

    
    lines = base.mark_line().encode(
        y=alt.Y('Close', title='收盤價'),
        color=alt.value('blue')
    )
    base = alt.Chart(stock_data).encode(x='Date:T')
    st.altair_chart(lines, use_container_width=True)
    # 常數
    stock_count = 12   
    already_money = 50000 
    
    # 獲取 VWRA.L 股價
    vwra_stock_price = get_stock_price('VWRA.L')

    usd_twd_exchange_rate = get_exchange_rate('USD', 'TWD')  # 注意這只是範例
    

    
    st.write(f"VWRA.L 的股價: ${vwra_stock_price:.2f}")
    st.write(f"美元兌台幣匯率: {usd_twd_exchange_rate:.2f}")
    st.write("------------------")      
    
    st.write(f"持有數量: {stock_count:}")
    stock_sum = stock_count*vwra_stock_price*usd_twd_exchange_rate

    st.write("------------------")      
    st.write(f"股票價值: {stock_sum:.2f}")
    st.write(f"台幣餘額: {195:.2f}")    
    st.write("------------------")  
    st.write(f"已投資金額: {already_money:.2f}")
    st.write("------------------")  
    # 建立表格資料
    data = {
        "時間": [ "(2024)113/08/06"],
        "成交價格": [ f"${126.46:.2f}"],
        "成交數量": [ 12],
        "手續費": [ f"${3.79:.2f}"],
        "美金成本": [f"${1521.31:.2f}"],
        "台幣成本": [ f"${49805:.2f}"],
        "匯率": [ f"{32.74:.2f}"]
    }
    
    # 將資料轉換為 DataFrame
    df = pd.DataFrame(data)
    
    # 顯示表格
    st.table(df)  # 使用 .T 轉置 DataFrame 以顯示欄位名稱為列名
if __name__ == "__main__":
    main()


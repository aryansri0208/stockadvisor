# app.py

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.title("Stock Analysis Dashboard")

# Input for stock ticker
stock_ticker = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL, MSFT):", "AAPL")

# Date range selection
start_date = st.date_input("Start Date", datetime(2022, 1, 1))
end_date = st.date_input("End Date", datetime.now())

if st.button("Analyze Stock"):
    with st.spinner("Analyzing stock..."):
        # Fetch data from the FastAPI backend
        response = requests.get(f"http://localhost:8000/analyze_stock/{stock_ticker}?start_date={start_date}&end_date={end_date}")
        if response.status_code == 200:
            data = response.json()
            stock_data = pd.DataFrame(data["stock_data"])
            prophet_forecast = pd.DataFrame(data["prophet_forecast"])

            # Ensure 'Date' columns are datetime objects
            stock_data['Date'] = pd.to_datetime(stock_data['Date'])
            prophet_forecast['ds'] = pd.to_datetime(prophet_forecast['ds'])

            st.subheader("Closing Price")
            fig = px.line(stock_data, x='Date', y='Adj Close', title=f'Closing Price of {stock_ticker}')
            st.plotly_chart(fig)

            st.subheader("Volume")
            fig = px.line(stock_data, x='Date', y='Volume', title=f'Sales Volume for {stock_ticker}')
            st.plotly_chart(fig)

            st.subheader("Moving Averages")
            ma_day = [10, 20, 50]
            for ma in ma_day:
                stock_data[f"MA for {ma} days"] = stock_data['Adj Close'].rolling(ma).mean()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Adj Close'], mode='lines', name='Adj Close'))
            for ma in ma_day:
                fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data[f"MA for {ma} days"], mode='lines', name=f'MA {ma} days'))
            fig.update_layout(title=f'Moving Averages of {stock_ticker}')
            st.plotly_chart(fig)

            st.subheader("Daily Return")
            stock_data['Daily Return'] = stock_data['Adj Close'].pct_change()
            fig = px.line(stock_data, x='Date', y='Daily Return', title=f"Daily Return of {stock_ticker}")
            st.plotly_chart(fig)

            st.subheader("Daily Return Histogram")
            stock_data['Daily Return'] = stock_data['Adj Close'].pct_change()
            fig = px.histogram(stock_data, x='Daily Return', nbins=50, title=f'Daily Return Histogram of {stock_ticker}')
            st.plotly_chart(fig)

            st.subheader("Prophet Forecast")
            fig = px.line(prophet_forecast, x='ds', y='yhat', title=f'Prophet Forecast for {stock_ticker}')
            fig.add_scatter(x=prophet_forecast['ds'], y=prophet_forecast['yhat_lower'], mode='lines', name='yhat_lower')
            fig.add_scatter(x=prophet_forecast['ds'], y=prophet_forecast['yhat_upper'], mode='lines', name='yhat_upper')
            st.plotly_chart(fig)

        else:
            st.error("Error analyzing stock")

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

st.title("Stock Analysis Dashboard")

# Input for the main stock ticker
stock_ticker = st.text_input("Enter Stock Ticker Symbol for Analysis (e.g., AAPL):", "AAPL")

# Input for additional tickers for correlation analysis
correlation_tickers = st.text_input("Enter Additional Ticker Symbols for Correlation Analysis separated by commas (e.g., MSFT, GOOGL, AMZN):", "MSFT, GOOGL, AMZN")

# Date range selection
start_date = st.date_input("Start Date", datetime(2022, 1, 1))
end_date = st.date_input("End Date", datetime.now())

if st.button("Analyze Stock"):
    if not stock_ticker:
        st.error("Please enter a stock ticker for analysis.")
    else:
        with st.spinner("Analyzing stock..."):
            # Fetch data from the FastAPI backend
            response = requests.get(f"http://localhost:8000/analyze_stocks/?stock_tickers={stock_ticker}&correlation_tickers={correlation_tickers}&start_date={start_date}&end_date={end_date}")
            if response.status_code == 200:
                data = response.json()
                stock_data = pd.DataFrame(data["stock_data"])
                volume_data = pd.DataFrame(data["volume_data"])
                forecast_data = data["forecast_data"]
                correlation_matrix = pd.DataFrame(data["correlation_matrix"])

                # Ensure 'Date' columns are datetime objects
                stock_data['Date'] = pd.to_datetime(stock_data['Date'])
                volume_data['Date'] = pd.to_datetime(volume_data['Date'])

                ticker = stock_ticker.strip()
                if ticker not in stock_data.columns:
                    st.error(f"No data found for ticker {ticker}")
                else:
                    st.subheader(f"Analysis for {ticker}")

                    st.write(f"### Closing Prices")
                    fig = px.line(stock_data, x='Date', y=ticker, title=f'Closing Price of {ticker}')
                    st.plotly_chart(fig)

                    st.write(f"### Volume")
                    fig = px.line(volume_data, x='Date', y=ticker, title=f'Sales Volume for {ticker}')
                    st.plotly_chart(fig)

                    st.write(f"### Moving Averages")
                    ma_day = [10, 20, 50]
                    for ma in ma_day:
                        stock_data[f"{ticker} MA for {ma} days"] = stock_data[ticker].rolling(ma).mean()
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data[ticker], mode='lines', name=f'{ticker} Adj Close'))
                    for ma in ma_day:
                        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data[f"{ticker} MA for {ma} days"], mode='lines', name=f'{ticker} MA {ma} days'))
                    fig.update_layout(title='Moving Averages')
                    st.plotly_chart(fig)

                    st.write(f"### Daily Return")
                    stock_data[f"{ticker} Daily Return"] = stock_data[ticker].pct_change()
                    fig = px.line(stock_data, x='Date', y=f"{ticker} Daily Return", title=f"Daily Return of {ticker}")
                    st.plotly_chart(fig)

                    st.write(f"### Daily Return Histogram")
                    fig = px.histogram(stock_data, x=f"{ticker} Daily Return", nbins=50, title=f'Daily Return Histogram of {ticker}')
                    st.plotly_chart(fig)

                    st.write(f"### Prophet Forecast for {ticker}")
                    forecast_df = pd.DataFrame(forecast_data[ticker])
                    forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])

                    # Apply rolling mean for smoothing
                    forecast_df['yhat_smooth'] = forecast_df['yhat'].rolling(window=7).mean()
                    forecast_df['yhat_lower_smooth'] = forecast_df['yhat_lower'].rolling(window=7).mean()
                    forecast_df['yhat_upper_smooth'] = forecast_df['yhat_upper'].rolling(window=7).mean()
                    
                    fig = px.line(forecast_df, x='ds', y='yhat_smooth', title=f'Prophet Forecast for {ticker}')
                    fig.add_scatter(x=forecast_df['ds'], y=forecast_df['yhat_lower_smooth'], mode='lines', name='yhat_lower_smooth')
                    fig.add_scatter(x=forecast_df['ds'], y=forecast_df['yhat_upper_smooth'], mode='lines', name='yhat_upper_smooth')
                    st.plotly_chart(fig)

                st.subheader("Correlation Heatmap")
                plt.figure(figsize=(10, 8))
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
                plt.title('Correlation Heatmap')
                st.pyplot(plt.gcf())

            else:
                st.error("Error analyzing stock")

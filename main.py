from fastapi import FastAPI, HTTPException, Query
import yfinance as yf
import pandas as pd
from datetime import datetime
from prophet import Prophet

app = FastAPI()

@app.get("/analyze_stocks/")
def analyze_stocks(stock_tickers: str, correlation_tickers: str, start_date: str = Query(...), end_date: str = Query(...)):
    tickers = stock_tickers.split(',')
    correlation_tickers = correlation_tickers.split(',') if correlation_tickers else tickers
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    stock_data = {}
    volume_data = {}
    forecast_data = {}
    for ticker in tickers:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            raise HTTPException(status_code=404, detail=f"Stock ticker {ticker} not found or no data available")
        stock_data[ticker] = data['Adj Close']
        volume_data[ticker] = data['Volume']
        try:
            forecast_data[ticker] = prophet_forecast(data)
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))

    correlation_data = {}
    for ticker in correlation_tickers:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            raise HTTPException(status_code=404, detail=f"Stock ticker {ticker} not found or no data available")
        correlation_data[ticker] = data['Adj Close']

    stock_df = pd.DataFrame(stock_data)
    stock_df.reset_index(inplace=True)
    volume_df = pd.DataFrame(volume_data)
    volume_df.reset_index(inplace=True)
    
    correlation_df = pd.DataFrame(correlation_data)
    correlation_df.reset_index(inplace=True)

    combined_df = stock_df.merge(correlation_df, on='Date', how='outer')
    combined_df.set_index('Date', inplace=True)
    correlation_matrix = combined_df.corr()

    return {
        "stock_data": stock_df.to_dict(orient='records'),
        "volume_data": volume_df.to_dict(orient='records'),
        "forecast_data": forecast_data,
        "correlation_matrix": correlation_matrix.to_dict()
    }

def prophet_forecast(stock_data):
    prophet_data = stock_data.reset_index().rename(columns={'Date': 'ds', 'Adj Close': 'y'})
    if 'ds' not in prophet_data or 'y' not in prophet_data:
        raise ValueError("Dataframe must have columns 'ds' and 'y' with the dates and values respectively.")
    model = Prophet()
    model.fit(prophet_data)
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    
    # Apply rolling mean for smoothing
    forecast['yhat_smooth'] = forecast['yhat'].rolling(window=7).mean()
    forecast['yhat_lower_smooth'] = forecast['yhat_lower'].rolling(window=7).mean()
    forecast['yhat_upper_smooth'] = forecast['yhat_upper'].rolling(window=7).mean()
    
    return forecast.tail(365).to_dict(orient='records')

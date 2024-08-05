# main.py

from fastapi import FastAPI, HTTPException, Query
import yfinance as yf
import pandas as pd
from datetime import datetime
from prophet import Prophet

app = FastAPI()

@app.get("/analyze_stock/{stock_ticker}")
def analyze_stock(stock_ticker: str, start_date: str = Query(...), end_date: str = Query(...)):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    stock_data = yf.download(stock_ticker, start=start, end=end)
    if stock_data.empty:
        raise HTTPException(status_code=404, detail="Stock ticker not found or no data available")

    stock_data.reset_index(inplace=True)
    data = stock_data.to_dict(orient='records')
    
    # Prophet Forecast
    prophet_forecast_data = prophet_forecast(stock_data)
    
    return {
        "stock_data": data,
        "prophet_forecast": prophet_forecast_data
    }

def prophet_forecast(stock_data):
    prophet_data = stock_data.rename(columns={'Date': 'ds', 'Adj Close': 'y'})
    model = Prophet()
    model.fit(prophet_data)
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(365)
    return forecast.to_dict(orient='records')

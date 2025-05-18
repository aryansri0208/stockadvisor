from fastapi import FastAPI, HTTPException, Query
import yfinance as yf
import pandas as pd
from datetime import datetime
from prophet import Prophet

app = FastAPI()

@app.get("/analyze_stocks/")
def analyze_stocks(stock_tickers: str, correlation_tickers: str, start_date: str = Query(...), end_date: str = Query(...)):
    tickers = [t.strip() for t in stock_tickers.split(',')]
    correlation_tickers = [t.strip() for t in correlation_tickers.split(',')] if correlation_tickers else tickers
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    stock_data = pd.DataFrame()
    volume_data = pd.DataFrame()
    forecast_data = {}
    
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start, end=end)
            if data.empty:
                raise HTTPException(status_code=404, detail=f"Stock ticker {ticker} not found or no data available")
            stock_data[ticker] = data['Close']  # Changed from 'Adj Close' to 'Close'
            volume_data[ticker] = data['Volume']
            try:
                forecast_data[ticker] = prophet_forecast(data.reset_index(), ticker)
            except ValueError as e:
                raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching data for {ticker}: {str(e)}")

    correlation_data = pd.DataFrame()
    for ticker in correlation_tickers:
        if ticker not in stock_data.columns:  # Only download if not already fetched
            try:
                data = yf.download(ticker, start=start, end=end)
                if data.empty:
                    raise HTTPException(status_code=404, detail=f"Stock ticker {ticker} not found or no data available")
                correlation_data[ticker] = data['Close']  # Changed from 'Adj Close' to 'Close'
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error fetching data for {ticker}: {str(e)}")

    stock_df = stock_data.reset_index()
    volume_df = volume_data.reset_index()
    
    # Combine stock data with correlation data
    if not correlation_data.empty:
        correlation_df = correlation_data.reset_index()
        combined_df = pd.concat([stock_df.set_index('Date'), correlation_df.set_index('Date')], axis=1)
    else:
        combined_df = stock_df.set_index('Date')
    
    correlation_matrix = combined_df.corr()

    return {
        "stock_data": stock_df.to_dict(orient='records'),
        "volume_data": volume_df.to_dict(orient='records'),
        "forecast_data": forecast_data,
        "correlation_matrix": correlation_matrix.to_dict()
    }

def prophet_forecast(stock_data, ticker):
    prophet_data = pd.DataFrame()
    prophet_data['ds'] = stock_data['Date']
    prophet_data['y'] = stock_data['Close']  # Changed from 'Adj Close' to 'Close'
    
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

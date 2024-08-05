import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
from sklearn.metrics import mean_absolute_error, mean_squared_error
from keras.models import Sequential
from keras.layers import Dense, LSTM

sns.set_style('whitegrid')
plt.style.use("fivethirtyeight")

def plot_closing_price(stock_data, stock_ticker):
    plt.figure(figsize=(15, 10))
    stock_data['Adj Close'].plot()
    plt.ylabel('Adj Close')
    plt.title(f"Closing Price of {stock_ticker}")
    plt.tight_layout()
    plt.savefig(f"{stock_ticker}_Closing_Price.png")

def plot_volume(stock_data, stock_ticker):
    plt.figure(figsize=(15, 10))
    stock_data['Volume'].plot()
    plt.ylabel('Volume')
    plt.title(f"Sales Volume for {stock_ticker}")
    plt.tight_layout()
    plt.savefig(f"{stock_ticker}_Volume.png")

def plot_moving_averages(stock_data, stock_ticker):
    ma_day = [10, 20, 50]
    for ma in ma_day:
        column_name = f"MA for {ma} days"
        stock_data[column_name] = stock_data['Adj Close'].rolling(ma).mean()

    plt.figure(figsize=(15, 10))
    stock_data[['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']].plot()
    plt.title(f'Moving Averages of {stock_ticker}')
    plt.tight_layout()
    plt.savefig(f"{stock_ticker}_Moving_Averages.png")

def plot_daily_return(stock_data, stock_ticker):
    stock_data['Daily Return'] = stock_data['Adj Close'].pct_change()

    plt.figure(figsize=(12, 9))
    stock_data['Daily Return'].plot(legend=True, linestyle='--', marker='o')
    plt.title(f"Daily Return of {stock_ticker}")
    plt.tight_layout()
    plt.savefig(f"{stock_ticker}_Daily_Return.png")

def plot_daily_return_histogram(stock_data, stock_ticker):
    plt.figure(figsize=(12, 9))
    stock_data['Daily Return'].hist(bins=50)
    plt.xlabel('Daily Return')
    plt.ylabel('Counts')
    plt.title(f'Daily Return Histogram of {stock_ticker}')
    plt.tight_layout()
    plt.savefig(f"{stock_ticker}_Daily_Return_Histogram.png")

def prophet_forecast(stock_data, stock_ticker):
    prophet_data = stock_data.reset_index().rename(columns={'Date': 'ds', 'Adj Close': 'y'})
    model = Prophet()
    model.fit(prophet_data)
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    fig1 = model.plot(forecast)
    plt.title(f'Stock Price Forecast using Prophet for {stock_ticker}')
    plt.xlabel('Date')
    plt.ylabel('Close Price USD ($)')
    plt.savefig(f"{stock_ticker}_Prophet_Prediction.png")

    fig2 = model.plot_components(forecast)
    plt.savefig(f"{stock_ticker}_Prophet_Components.png")

def prophet_current_prediction(stock_data, stock_ticker):
    train_data = stock_data.iloc[:-365]
    test_data = stock_data.iloc[-365:]

    prophet_data = train_data.reset_index().rename(columns={'Date': 'ds', 'Adj Close': 'y'})
    model = Prophet()
    model.fit(prophet_data)

    future = pd.DataFrame(test_data.index).rename(columns={test_data.index.name: 'ds'})
    forecast = model.predict(future)

    # Align forecast with test data
    forecast.index = test_data.index

    plt.figure(figsize=(15, 10))
    plt.plot(test_data.index, test_data['Adj Close'], label='Actual')
    plt.plot(test_data.index, forecast['yhat'], label='Predicted', linestyle='--')
    plt.fill_between(test_data.index, forecast['yhat_lower'], forecast['yhat_upper'], color='gray', alpha=0.2)
    plt.title(f'Actual vs Predicted Closing Price for {stock_ticker}')
    plt.xlabel('Date')
    plt.ylabel('Close Price USD ($)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{stock_ticker}_Actual_vs_Predicted.png")

    y_true = test_data['Adj Close']
    y_pred = forecast['yhat']
    
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    print(f'MAE: {mae}')
    print(f'RMSE: {rmse}')

    # Calculate percentage error
    percentage_error = ((y_true - y_pred) / y_true) * 100

    plt.figure(figsize=(10, 5))
    plt.plot(test_data.index, percentage_error, label='Percentage Error', linestyle='--', marker='o')
    plt.title(f'Percentage Error of Prophet Model for {stock_ticker}')
    plt.xlabel('Date')
    plt.ylabel('Percentage Error (%)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{stock_ticker}_Prophet_Percentage_Error.png")

def lstm_forecast(stock_data, stock_ticker):
    data = stock_data.filter(['Adj Close'])
    dataset = data.values
    training_data_len = int(np.ceil(len(dataset) * .95))

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    train_data = scaled_data[0:int(training_data_len), :]
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, batch_size=1, epochs=1)

    test_data = scaled_data[training_data_len - 60:, :]
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions

    plt.figure(figsize=(16, 6))
    plt.title(f'LSTM Model Predictions for {stock_ticker}')
    plt.xlabel('Date')
    plt.ylabel('Close Price USD ($)')
    plt.plot(train['Adj Close'])
    plt.plot(valid[['Adj Close', 'Predictions']])
    plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
    plt.tight_layout()
    plt.savefig(f"{stock_ticker}_LSTM_Predictions.png")

def analyze_stock(stock_ticker):
    end = datetime.now() - timedelta(days=1)  # Till present day
    start = datetime(end.year - 2, end.month, end.day)

    stock_data = yf.download(stock_ticker, start=start, end=end)
    
    plot_closing_price(stock_data, stock_ticker)
    plot_volume(stock_data, stock_ticker)
    plot_moving_averages(stock_data, stock_ticker)
    plot_daily_return(stock_data, stock_ticker)
    plot_daily_return_histogram(stock_data, stock_ticker)
    prophet_forecast(stock_data, stock_ticker)
    prophet_current_prediction(stock_data, stock_ticker)

# Example usage
analyze_stock('AAPL')

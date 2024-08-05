# Stock Analysis Application

This project is a web application for analyzing and forecasting stock prices. It uses FastAPI for the backend and Streamlit for the frontend to provide an interactive user interface. The application fetches stock data from Yahoo Finance, calculates various metrics, and provides visualizations and forecasts using Prophet.

## Features

- Fetches historical stock data for two user-specified stocks.
- Displays closing prices, volume, moving averages, and daily returns.
- Provides histograms of daily returns.
- Generates forecasts using the Prophet model.
- Calculates and displays the correlation between the two stocks.

## Installation

### Prerequisites

- Python 3.8 or later
- Git
- Pip

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/aryansri0208/stockadvisor.git
    cd stockadvisor
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Start the FastAPI backend:**

    ```bash
    uvicorn main:app --reload
    ```

    The backend will be available at `http://localhost:8000`.

2. **Start the Streamlit frontend:**

    ```bash
    streamlit run app.py
    ```

    The frontend will be available at `http://localhost:8501`.

## API Endpoints

- **Analyze Stock:** Fetches data for a stock, calculates correlation, and generates forecasts.

    ```http
    GET /analyze_stock/?stock_ticker={stock_ticker}&second_stock_ticker={second_stock_ticker}&start_date={start_date}&end_date={end_date}
    ```

    - **Parameters:**
        - `stock_ticker` (string): The ticker symbol of the primary stock (e.g., `AAPL`).
        - `start_date` (string): The start date for the analysis in `YYYY-MM-DD` format.
        - `end_date` (string): The end date for the analysis in `YYYY-MM-DD` format.

    - **Response:**
        - `stock_data`: Historical data for the primary stock.
        - `second_stock_data`: Historical data for the second stock.
        - `prophet_forecast`: Forecast data for the primary stock.
        - `correlation`: Correlation value between the two stocks.

## File Structure

Creating a comprehensive README file for your project is crucial for explaining its purpose, usage, and how to set it up. Here’s a sample README.md file for your stock analysis application:

markdown
Copy code
# Stock Analysis Application

This project is a web application for analyzing and forecasting stock prices. It uses FastAPI for the backend and Streamlit for the frontend to provide an interactive user interface. The application fetches stock data from Yahoo Finance, calculates various metrics, and provides visualizations and forecasts using Prophet.

## Features

- Fetches historical stock data for two user-specified stocks.
- Displays closing prices, volume, moving averages, and daily returns.
- Provides histograms of daily returns.
- Generates forecasts using the Prophet model.
- Calculates and displays the correlation between the two stocks.

## Installation

### Prerequisites

- Python 3.8 or later
- Git
- Pip

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/aryansri0208/stockadvisor.git
    cd stockadvisor
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Start the FastAPI backend:**

    ```bash
    uvicorn main:app --reload
    ```

    The backend will be available at `http://localhost:8000`.

2. **Start the Streamlit frontend:**

    ```bash
    streamlit run app.py
    ```

    The frontend will be available at `http://localhost:8501`.

## API Endpoints

- **Analyze Stock:** Fetches data for two stocks, calculates correlation, and generates forecasts.

    ```http
    GET /analyze_stock/?stock_ticker={stock_ticker}&second_stock_ticker={second_stock_ticker}&start_date={start_date}&end_date={end_date}
    ```

    - **Parameters:**
        - `stock_ticker` (string): The ticker symbol of the primary stock (e.g., `AAPL`).
        - `second_stock_ticker` (string): The ticker symbol of the second stock (e.g., `MSFT`).
        - `start_date` (string): The start date for the analysis in `YYYY-MM-DD` format.
        - `end_date` (string): The end date for the analysis in `YYYY-MM-DD` format.

    - **Response:**
        - `stock_data`: Historical data for the primary stock.
        - `second_stock_data`: Historical data for the second stock.
        - `prophet_forecast`: Forecast data for the primary stock.
        - `correlation`: Correlation value between the two stocks.

## File Structure

stockadvisor/
├── .venv/ # Virtual environment directory
├── .gitignore # Git ignore file
├── README.md # README file
├── requirements.txt # Python dependencies
├── main.py # FastAPI backend script
└── app.py # Streamlit frontend script



## Contributing

Contributions are welcome! Please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License.

## Contact

For any questions or inquiries, please contact [aryansri0208](mailto:aryansri0208@example.com).

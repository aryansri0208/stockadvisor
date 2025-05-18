# Stock Advisor Application

A powerful stock analysis tool that provides real-time stock data visualization, technical analysis, and price forecasting using Machine Learning.

## Features

- Real-time stock data visualization
- Technical analysis with moving averages
- Stock price forecasting using Facebook Prophet
- Correlation analysis between multiple stocks
- Volume analysis
- Interactive charts and visualizations
- Daily return analysis and distribution

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd stockadvisor
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

1. Start the FastAPI backend server:
```bash
uvicorn main:app --reload
```
The backend API will be available at http://localhost:8000

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run app.py
```
The web interface will automatically open in your default browser at http://localhost:8501

## Usage

1. Enter a stock ticker symbol (e.g., AAPL for Apple Inc.)
2. Add additional tickers for correlation analysis (optional)
3. Select the date range for analysis
4. Click "Analyze Stock" to generate:
   - Stock price trends
   - Volume analysis
   - Moving averages (10, 20, and 50-day)
   - Daily returns analysis
   - Price forecasts
   - Correlation heatmap

## API Endpoints

### GET /analyze_stocks/
Parameters:
- stock_tickers (str): Main stock ticker(s) to analyze
- correlation_tickers (str): Additional tickers for correlation analysis
- start_date (str): Analysis start date (YYYY-MM-DD)
- end_date (str): Analysis end date (YYYY-MM-DD)

## Technologies Used

- FastAPI: Backend API framework
- Streamlit: Frontend interface
- yfinance: Real-time stock data
- Facebook Prophet: Time series forecasting
- Pandas: Data manipulation
- Plotly: Interactive visualizations
- Seaborn: Statistical visualizations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

from flask import Flask, render_template, request
import yfinance as yf
import plotly.graph_objs as go
from plotly.offline import plot

app = Flask(__name__)

def get_stock_data(ticker_symbol):
    """
    Fetch stock information for the given ticker symbol.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        stock_info = stock.info

        # Basic Stock Info
        data = {
            "name": stock_info.get('longName', 'N/A'),
            "symbol": ticker_symbol,
            "sector": stock_info.get('sector', 'N/A'),
            "current_price": stock_info.get('currentPrice', 'N/A'),
            "market_cap": stock_info.get('marketCap', 'N/A'),
            "pe_ratio": stock_info.get('trailingPE', 'N/A'),
            "pb_ratio": stock_info.get('priceToBook', 'N/A'),
            "revenue_growth": stock_info.get('revenueGrowth', 'N/A'),
            "profit_margin": stock_info.get('profitMargins', 'N/A'),
            "roe": stock_info.get('returnOnEquity', 'N/A'),
            "debt_to_equity": stock_info.get('debtToEquity', 'N/A'),
            "recommendation": stock_info.get('recommendationKey', 'N/A')
        }

        # Calculate Buy Score (example calculation)
        buy_score = calculate_buy_score(data)
        data['buy_score'] = buy_score

        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def calculate_buy_score(stock_data):
    """
    Calculate the buy score based on financial metrics.
    """
    score = 0
    if stock_data['pe_ratio'] and stock_data['pe_ratio'] < 15:
        score += 5
    elif stock_data['pe_ratio'] and stock_data['pe_ratio'] < 25:
        score += 3
    
    if stock_data['pb_ratio'] and stock_data['pb_ratio'] < 1:
        score += 5
    elif stock_data['pb_ratio'] and stock_data['pb_ratio'] < 3:
        score += 3

    if stock_data['revenue_growth'] and stock_data['revenue_growth'] > 0.1:
        score += 5
    elif stock_data['revenue_growth'] and stock_data['revenue_growth'] > 0:
        score += 3

    if stock_data['profit_margin'] and stock_data['profit_margin'] > 0.2:
        score += 5
    elif stock_data['profit_margin'] and stock_data['profit_margin'] > 0.1:
        score += 3

    if stock_data['roe'] and stock_data['roe'] > 0.15:
        score += 5
    elif stock_data['roe'] and stock_data['roe'] > 0.1:
        score += 3

    if stock_data['debt_to_equity'] and stock_data['debt_to_equity'] < 0.5:
        score += 5
    elif stock_data['debt_to_equity'] and stock_data['debt_to_equity'] < 1:
        score += 3

    return score

def get_candlestick_data(ticker_symbol):
    """
    Fetch historical stock data for candlestick chart.
    """
    stock = yf.Ticker(ticker_symbol)
    hist = stock.history(period="1mo")  # You can adjust the period here
    data = [
        go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            increasing_line_color='green',
            decreasing_line_color='red',
            name=f"{ticker_symbol} Candlestick"
        )
    ]
    layout = go.Layout(title=f"{ticker_symbol} Stock Candlestick Chart", xaxis=dict(title="Date"), yaxis=dict(title="Price"))
    fig = go.Figure(data=data, layout=layout)
    chart = plot(fig, output_type='div')
    return chart

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stock', methods=['POST'])
def stock():
    ticker = request.form['ticker']
    stock_data = get_stock_data(ticker)
    if stock_data:
        # Fetch the candlestick chart HTML div for the stock
        candlestick_chart = get_candlestick_data(ticker)
        return render_template('stock_info.html', stock_data=stock_data, candlestick_chart=candlestick_chart)
    else:
        return "Error fetching data", 400

if __name__ == '__main__':
    app.run(debug=True)

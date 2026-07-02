from flask import Flask, render_template, jsonify, request
import yfinance as yf
import time
import random
import math
import threading

app = Flask(__name__)

# Config for real-market stock tickers
TICKER_INFO = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corp.',
    'GOOGL': 'Alphabet Inc.',
    'AMZN': 'Amazon.com Inc.'
}

# Global cache for stock data to avoid Yahoo Finance rate limits
stock_cache = {
    'last_updated': 0,
    'data': None
}

# Thread lock to prevent cache stampedes under concurrent traffic
cache_lock = threading.Lock()

def generate_agy_stock():
    """Generates a beautiful upwards-trending custom stock for Antigravity Corp. dynamically on each request."""
    t = time.time()
    history = []
    # Compute 10 historical points using an algorithm that creates an elegant upward trend
    for i in range(10):
        # Stepping price up with deterministic sine wave variations
        price = 230.0 + (i * 2.05) + math.sin((t // 1000 + i) * 0.8) * 1.3
        history.append(round(price, 2))
        
    # Apply minor real-time fluctuation to the current price
    fluctuation = math.sin(t / 15.0) * 0.7 + (random.random() - 0.5) * 0.2
    history[-1] = round(history[-1] + fluctuation, 2)
    
    current_price = history[-1]
    prev_price = history[-2]
    change_percent = ((current_price - prev_price) / prev_price) * 100
    
    return {
        'symbol': 'AGY',
        'name': 'Antigravity Corp.',
        'price': round(current_price, 2),
        'change_percent': round(change_percent, 2),
        'history': history
    }

def fetch_real_stock_data():
    """Fetches real-market stock data using yfinance."""
    data = []
    for symbol, name in TICKER_INFO.items():
        ticker = yf.Ticker(symbol)
        # Fetch 5 days of history to get closing prices and daily trends
        hist = ticker.history(period="5d")
        if hist.empty:
            raise Exception(f"No history returned for {symbol}")
            
        close_prices = hist['Close'].dropna().tolist()
        if not close_prices:
            raise Exception(f"No closing prices available for {symbol}")
            
        # Standardize history to up to 10 points
        history_list = [float(p) for p in close_prices[-10:]]
        current_price = float(history_list[-1])
        
        # Calculate percentage change from previous day's close
        if len(close_prices) >= 2:
            prev_price = float(close_prices[-2])
            change_percent = ((current_price - prev_price) / prev_price) * 100
        else:
            change_percent = 0.0
            
        data.append({
            'symbol': symbol,
            'name': name,
            'price': round(current_price, 2),
            'change_percent': round(change_percent, 2),
            'history': [round(p, 2) for p in history_list]
        })
        
    return data

def generate_fallback_stock_data():
    """Generates a premium-looking, time-stable simulated dataset as a fallback."""
    fallback_tickers = {
        'AAPL': ('Apple Inc.', 185.50, True),
        'MSFT': ('Microsoft Corp.', 415.20, False),
        'GOOGL': ('Alphabet Inc.', 172.80, True),
        'AMZN': ('Amazon.com Inc.', 178.40, True)
    }
    
    data = []
    t = time.time()
    # Use a localized thread-safe random generator to avoid compromising global security tokens
    local_random = random.Random(int(t) // 35)
    
    for symbol, (name, base, is_up) in fallback_tickers.items():
        prices = []
        curr = base
        trend_direction = 1 if is_up else -1
        for _ in range(10):
            step = (local_random.random() - 0.45) * 1.5 + (0.15 * trend_direction)
            curr += step
            prices.append(round(curr, 2))
            
        current_price = prices[-1]
        prev_price = prices[-2]
        change_percent = ((current_price - prev_price) / prev_price) * 100
        
        data.append({
            'symbol': symbol,
            'name': name,
            'price': round(current_price, 2),
            'change_percent': round(change_percent, 2),
            'history': prices
        })
        
    return data


@app.route('/')
def index():
    # Mock data for the bank dashboard
    account_info = {
        'owner': 'Aurelia Thorne',
        'checking_balance': '$5,432.10',
        'savings_balance': '$123,456.78',
        'credit_card_balance': '$432.10',
    }
    transactions = [
        {
            'date': '2026-06-30',
            'description': 'Coffee Shop',
            'amount': '-$4.50',
            'category': 'Food',
            'type': 'debit',
        },
        {
            'date': '2026-06-29',
            'description': 'Salary Deposit',
            'amount': '+$5,000.00',
            'category': 'Income',
            'type': 'credit',
        },
        {
            'date': '2026-06-28',
            'description': 'Online Retailer',
            'amount': '-$89.99',
            'category': 'Shopping',
            'type': 'debit',
        },
        {
            'date': '2026-06-25',
            'description': 'Gas Station',
            'amount': '-$45.00',
            'category': 'Transport',
            'type': 'debit',
        },
    ]
    return render_template(
        'index.html', account=account_info, transactions=transactions
    )


@app.route('/api/stocks')
def get_stocks():
    global stock_cache
    now = time.time()
    
    # Check if forced cache refresh is requested
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    # Refresh cache if empty, expired (5 minutes), or forced
    if force_refresh or stock_cache['data'] is None or (now - stock_cache['last_updated'] > 300):
        with cache_lock:
            # Double-checked locking pattern
            if force_refresh or stock_cache['data'] is None or (now - stock_cache['last_updated'] > 300):
                try:
                    stock_cache['data'] = fetch_real_stock_data()
                    stock_cache['last_updated'] = now
                except Exception as e:
                    print(f"yfinance fetch failed: {e}. Falling back to simulated data.")
                    # Temporarily cache fallback data for 30s to prevent constant blocking retry storms
                    stock_cache['data'] = generate_fallback_stock_data()
                    stock_cache['last_updated'] = now - 270 # Retry in 30 seconds
            
    # Copy cached list and append custom AGY dynamically to allow real-time micro-fluctuations
    response_data = list(stock_cache['data'])
    response_data.append(generate_agy_stock())
    
    return jsonify(response_data)


if __name__ == '__main__':
    # Running on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)


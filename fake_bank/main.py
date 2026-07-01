import os
import json
import time
import random
from flask import Flask, render_template
import yfinance as yf

app = Flask(__name__)

# Tracked stock tickers
TICKERS = ['JPM', 'BAC', 'GS', 'WFC', 'MS', 'C']

# Predefined metadata for bank stocks (used as fallback and name dictionary)
BANK_METADATA = {
    'JPM': {'name': 'JPMorgan Chase', 'base_price': 195.40},
    'BAC': {'name': 'Bank of America', 'base_price': 38.50},
    'GS': {'name': 'Goldman Sachs', 'base_price': 455.20},
    'WFC': {'name': 'Wells Fargo', 'base_price': 58.25},
    'MS': {'name': 'Morgan Stanley', 'base_price': 98.15},
    'C': {'name': 'Citigroup', 'base_price': 61.40}
}

# State for mock rates to ensure smooth rolling updates if yfinance is blocked or disabled
MOCK_RATES_STATE = {}

def get_mock_rate(symbol):
    global MOCK_RATES_STATE
    metadata = BANK_METADATA[symbol]
    base_price = metadata['base_price']
    
    if symbol not in MOCK_RATES_STATE:
        price = base_price
        change_percent = random.uniform(-1.5, 1.5)
        change = price * (change_percent / 100.0)
        MOCK_RATES_STATE[symbol] = {
            'price': price,
            'change': change,
            'change_percent': change_percent,
            'prev_close': price - change
        }
    else:
        current_state = MOCK_RATES_STATE[symbol]
        prev_close = current_state['prev_close']
        fluctuation = random.uniform(-0.15, 0.15)  # slight fluctuation (-0.15% to +0.15%)
        
        new_price = current_state['price'] * (1 + fluctuation / 100.0)
        # Avoid drifting too far from original base price
        if new_price < base_price * 0.8:
            new_price = base_price * 0.8
        elif new_price > base_price * 1.2:
            new_price = base_price * 1.2
            
        new_change = new_price - prev_close
        new_change_percent = (new_change / prev_close) * 100.0
        
        MOCK_RATES_STATE[symbol] = {
            'price': new_price,
            'change': new_change,
            'change_percent': new_change_percent,
            'prev_close': prev_close
        }
        
    state = MOCK_RATES_STATE[symbol]
    return {
        'symbol': symbol,
        'name': metadata['name'],
        'price': round(state['price'], 2),
        'change': round(state['change'], 2),
        'change_percent': round(state['change_percent'], 2),
        'prev_close': round(state['prev_close'], 2)
    }


@app.route('/api/market-rates')
def get_market_rates():
    current_time = time.time()
    rates = {}
    is_mock = False
    
    try:
        # Fetch 2-day historical bulk data
        df = yf.download(TICKERS, period="2d", group_by="ticker", progress=False, timeout=5)
        
        # Check if we got data back
        if df is not None and not df.empty:
            for symbol in TICKERS:
                try:
                    if symbol in df.columns.levels[0]:
                        ticker_df = df[symbol].dropna()
                        if len(ticker_df) >= 2:
                            prev_close = float(ticker_df['Close'].iloc[-2])
                            current_price = float(ticker_df['Close'].iloc[-1])
                            change = current_price - prev_close
                            change_percent = (change / prev_close) * 100.0
                            
                            rates[symbol] = {
                                'symbol': symbol,
                                'name': BANK_METADATA[symbol]['name'],
                                'price': round(current_price, 2),
                                'change': round(change, 2),
                                'change_percent': round(change_percent, 2),
                                'prev_close': round(prev_close, 2)
                            }
                        elif len(ticker_df) == 1:
                            # If only one day of data is available, compute compared to preset base_price
                            current_price = float(ticker_df['Close'].iloc[0])
                            base_price = BANK_METADATA[symbol]['base_price']
                            change = current_price - base_price
                            change_percent = (change / base_price) * 100.0
                            
                            rates[symbol] = {
                                'symbol': symbol,
                                'name': BANK_METADATA[symbol]['name'],
                                'price': round(current_price, 2),
                                'change': round(change, 2),
                                'change_percent': round(change_percent, 2),
                                'prev_close': round(base_price, 2)
                            }
                        else:
                            rates[symbol] = get_mock_rate(symbol)
                            is_mock = True
                    else:
                        rates[symbol] = get_mock_rate(symbol)
                        is_mock = True
                except Exception as sym_err:
                    print(f"Error parsing ticker {symbol}: {sym_err}")
                    rates[symbol] = get_mock_rate(symbol)
                    is_mock = True
        else:
            # Empty dataframe
            is_mock = True
            for symbol in TICKERS:
                rates[symbol] = get_mock_rate(symbol)
    except Exception as e:
        print(f"yfinance download failed, falling back to mock: {e}")
        is_mock = True
        for symbol in TICKERS:
            rates[symbol] = get_mock_rate(symbol)
            
    response_data = {
        'timestamp': current_time,
        'is_mock': is_mock,
        'rates': rates
    }
    
    return app.response_class(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )


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


if __name__ == '__main__':
  # Running on port 5000
  app.run(host='0.0.0.0', port=5000, debug=True)

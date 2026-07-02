import unittest
import json
from unittest.mock import patch
from main import app, stock_cache

class FakeBankTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Reset cache before each test to ensure test isolation
        stock_cache['data'] = None
        stock_cache['last_updated'] = 0

    @patch('main.fetch_real_stock_data')
    def test_stocks_endpoint_success(self, mock_fetch):
        # Mock successful fetch from yfinance
        mock_data = [
            {
                'symbol': 'AAPL',
                'name': 'Apple Inc.',
                'price': 180.0,
                'change_percent': 1.5,
                'history': [178.0, 179.0, 180.0]
            },
            {
                'symbol': 'MSFT',
                'name': 'Microsoft Corp.',
                'price': 400.0,
                'change_percent': -0.5,
                'history': [402.0, 401.0, 400.0]
            },
            {
                'symbol': 'GOOGL',
                'name': 'Alphabet Inc.',
                'price': 150.0,
                'change_percent': 0.0,
                'history': [150.0, 150.0, 150.0]
            },
            {
                'symbol': 'AMZN',
                'name': 'Amazon.com Inc.',
                'price': 175.0,
                'change_percent': 2.0,
                'history': [171.5, 173.0, 175.0]
            }
        ]
        mock_fetch.return_value = mock_data
        
        response = self.app.get('/api/stocks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsInstance(data, list)
        
        # We expect mock_data symbols + 'AGY'
        expected_symbols = {'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'AGY'}
        symbols_returned = {stock['symbol'] for stock in data}
        self.assertEqual(expected_symbols, symbols_returned)
        
        for stock in data:
            self.assertIn('symbol', stock)
            self.assertIn('name', stock)
            self.assertIn('price', stock)
            self.assertIn('change_percent', stock)
            self.assertIn('history', stock)
            self.assertGreater(len(stock['history']), 0)
            
        mock_fetch.assert_called_once()

    @patch('main.fetch_real_stock_data')
    def test_stocks_endpoint_fallback(self, mock_fetch):
        # Mock yfinance fetch failure to trigger fallback simulation
        mock_fetch.side_effect = Exception("Yahoo Finance API Error")
        
        response = self.app.get('/api/stocks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsInstance(data, list)
        
        # Fallback should still return standard symbols + AGY
        expected_symbols = {'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'AGY'}
        symbols_returned = {stock['symbol'] for stock in data}
        self.assertEqual(expected_symbols, symbols_returned)
        
        for stock in data:
            self.assertIn('symbol', stock)
            self.assertIn('name', stock)
            self.assertIn('price', stock)
            self.assertIn('change_percent', stock)
            self.assertIn('history', stock)
            self.assertGreater(len(stock['history']), 0)

        mock_fetch.assert_called_once()

if __name__ == '__main__':
    unittest.main()

from flask import Flask, render_template

app = Flask(__name__)


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

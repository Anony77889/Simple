from flask import Flask, jsonify, request
from braintree import BraintreeGateway, Configuration, Environment

app = Flask(__name__)

# Configure Braintree
gateway = BraintreeGateway(
    Configuration(
        environment=Environment.Sandbox,
        merchant_id='your_merchant_id',
        public_key='your_public_key',
        private_key='your_private_key'
    )
)

@app.route('/token', methods=['GET'])
def generate_client_token():
    client_token = gateway.client_token.generate()
    return jsonify({'clientToken': client_token})

@app.route('/validate', methods=['POST'])
def validate_credit_card():
    data = request.json
    result = gateway.transaction.sale({
        'amount': '0.00',
        'payment_method_nonce': data['nonce'],
        'options': {
            'submit_for_settlement': False
        }
    })

    if result.is_success:
        return jsonify({'status': 'success', 'message': 'Card is valid.'})
    else:
        return jsonify({'status': 'error', 'message': result.message})

@app.route('/payment', methods=['POST'])
def process_payment():
    data = request.json
    result = gateway.transaction.sale({
        'amount': str(data['amount']),
        'payment_method_nonce': data['nonce'],
        'options': {
            'submit_for_settlement': True
        }
    })

    if result.is_success:
        return jsonify({'status': 'success', 'transaction_id': result.transaction.id})
    else:
        return jsonify({'status': 'error', 'message': result.message})

if __name__ == '__main__':
    app.run(debug=True)
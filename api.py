from flask import Flask, jsonify
from flask_cors import CORS

import db_queries
import main
from extract_params import *

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)


@app.route('/get_addresses', methods=['GET'])
def get_addresses():
    try:
        return jsonify({'addresses_and_balances': db_queries.get_addresses_and_balances()}), 200
    except:
        return '', 404


@app.route('/add_address', methods=['GET'])
def add_address():
    try:
        address = get_string_param('address')
        db_queries.add_address(address)
        return '', 200
    except:
        return '', 404


@app.route('/get_transactions/<address>', methods=['GET'])
def get_transactions(address):
    try:
        return jsonify(main.get_transactions(address)), 200
    except:
        return '', 404


@app.route('/sync', methods=['GET'])
def sync():
    try:
        main.sync()
        return '', 200
    except:
        return '', 404


@app.route('/detect_transfers', methods=['GET'])
def detect_transfers():
    try:
        return jsonify({'transfers': main.detect_transfers()}), 200
    except:
        return ', 404'


if __name__ == '__main__':
    db_queries.create_db()
    app.run(host='0.0.0.0', port=4000, debug=True)

import main

addresses = [
    {'hash': 'tx_id_1', 'wallet_id': 'wallet_id_1', 'time': '2020-01-01 15:30:20 UTC', 'balance_change': -5.3},
    # 5.3 BTC was withdrawn out of 'wallet_id_1'
    {'hash': 'tx_id_2', 'wallet_id': 'wallet_id_1', 'time': '2020-01-03 12:05:25 UTC', 'balance_change': 3.2},
    # 3.2 BTC was withdrawn out of 'wallet_id_1'
    {'hash': 'tx_id_3', 'wallet_id': 'wallet_id_2', 'time': '2020-01-01 15:30:20 UTC', 'balance_change': 5.3},
    # 5.3 BTC was deposited into 'wallet_id_2'
    {'hash': 'tx_id_4', 'wallet_id': 'wallet_id_3', 'time': '2020-01-01 15:30:20 UTC', 'balance_change': 5.3},
    # 5.3 BTC was deposited into 'wallet_id_3'
]
print(main.detect_transfers(addresses))

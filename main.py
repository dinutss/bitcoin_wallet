import requests
from collections import defaultdict
from datetime import datetime

import db_queries


def get_transactions(address):
    return db_queries.get_transactions(address)


def sync():
    for address in db_queries.get_addresses():
        sync_address(address)


def sync_address(address):
    # get transaction count
    tc_url = 'https://api.blockchair.com/bitcoin/dashboards/address/{}'.format(address)
    total_transaction_count = requests.get(tc_url).json()['data'][address]['address']['transaction_count']
    db_transaction_count = db_queries.get_number_of_transactions(address)
    transaction_count = total_transaction_count - db_transaction_count

    # get all transactions
    max_limit, max_offset = 10000, 1000000
    current_limit, current_offset = min(max_limit, transaction_count), 0
    transactions = []
    while transaction_count > 0 and current_offset <= max_offset:
        t_url = 'https://api.blockchair.com/bitcoin/dashboards/address/{}?limit={}&offset={}&transaction_details=true'.format(
            address, max_limit, current_offset)
        current_transactions = requests.get(t_url).json()['data'][address]['transactions']
        for t in current_transactions:
            t['wallet_id'] = address
            t['ts'] = datetime.strptime(t['time'], '%Y-%m-%d %H:%M:%S').timestamp()
        transactions.extend(current_transactions)
        transaction_count -= current_limit
        current_offset += current_limit
        current_limit = min(max_limit, transaction_count)
    db_queries.add_transactions(transactions)


def get_transactions_for_all_wallets(addresses: set) -> list:
    transactions = []
    for address in addresses:
        transactions.extend(get_transactions(address))
    return transactions


def detect_transfers():
    addresses = db_queries.get_addresses()
    transactions = get_transactions_for_all_wallets(addresses)

    d = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0, []])))
    for t in transactions:
        time, balance_change, wallet_id = t['time'], t['balance_change'], t['wallet_id']
        d[time][balance_change][wallet_id][0] += 1
        d[time][balance_change][wallet_id][1].append(t)

    transfers = []
    for time, time_values in d.items():
        for balance_change, bc_values in list(time_values.items()):
            for wallet_id1, wallet_id_values1 in list(bc_values.items()):
                opposite_balance_change = -1 * balance_change
                if not d.get(time).get(opposite_balance_change):
                    continue
                for wallet_id2, wallet_id_values2 in list(d[time][opposite_balance_change].items()):
                    if wallet_id1 == wallet_id2:
                        continue
                    if balance_change > opposite_balance_change:
                        transfers.append([wallet_id1, wallet_id2])
                    else:
                        transfers.append([wallet_id2, wallet_id1])
                    wallet_id_values1[0] -= 1
                    del wallet_id_values1[1][0]
                    if wallet_id_values1[0] == 0:
                        del d[time][balance_change][wallet_id1]
                    wallet_id_values2[0] -= 1
                    del wallet_id_values2[1][0]
                    if wallet_id_values2[0] == 0:
                        del d[time][opposite_balance_change][wallet_id2]
                    break
    return transfers

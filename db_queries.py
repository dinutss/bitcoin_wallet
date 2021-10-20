import sqlite3
from sqlite3 import Error

database = 'transactions.db'


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_db():
    sql_create_address_table = """ CREATE TABLE IF NOT EXISTS addresses(
                                        id integer PRIMARY KEY,
                                        name text NOT NULL UNIQUE
                                    ); """

    sql_create_transactions_table = """ CREATE TABLE IF NOT EXISTS transactions(
                                        block_id integer,
                                        hash text,
                                        ts timestamp,
                                        time text,
                                        balance_change integer,
                                        wallet_id text
                                    ); """
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_address_table)
        create_table(conn, sql_create_transactions_table)


def add_address(address):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    sql = """ INSERT INTO addresses (name) VALUES(?) """
    values = [address]
    c.execute(sql, values)
    conn.commit()


def get_addresses():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("""SELECT * FROM addresses ORDER BY id ASC""")
    rows = c.fetchall()
    addresses = []
    for row in rows:
        addresses.append(row[1])
    return addresses


def get_addresses_and_balances():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    addresses_and_balances = []
    for address in get_addresses():
        c.execute("""SELECT SUM(balance_change) FROM transactions WHERE wallet_id='{}';""".format(address))
        balance = c.fetchall()[0][0]
        if not balance:
            balance = 0
        addresses_and_balances.append([address, balance])
    return addresses_and_balances


def get_number_of_transactions(address):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    result = c.execute("""SELECT COUNT (*) FROM transactions WHERE wallet_id='{}'""".format(address))
    return result.fetchall()[0][0]


def add_transactions(transactions):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    for t in transactions:
        sql = """ INSERT INTO transactions (block_id,hash,ts,time,balance_change,wallet_id) VALUES(?,?,?,?,?,?) """
        values = [t['block_id'], t['hash'], t['ts'], t['time'], t['balance_change'], t['wallet_id']]
        c.execute(sql, values)
    conn.commit()


def get_transactions(address):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("""SELECT * FROM transactions WHERE wallet_id='{}' ORDER BY ts DESC""".format(address))
    rows = c.fetchall()
    keys, transactions = ['block_id', 'hash', 'ts', 'time', 'balance_change', 'wallet_id'], []
    for row in rows:
        transactions.append(dict(zip(keys, row)))
    return transactions

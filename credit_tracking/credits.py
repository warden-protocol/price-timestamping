import json
import sqlite3

import requests


def get_transactions(address, api_key):
    etherscan_url = "https://api-goerli.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    response = requests.get(etherscan_url, params=params)
    # Parse the JSON response and return a list of dictionaries with "from", "value", and "timestamp" fields
    transactions = json.loads(response.text)["result"]
    selected_fields = [{"hash": tx["hash"], "from": tx["from"],
                        "value": tx["value"], "timestamp": tx["timeStamp"]} for tx in transactions]
    return json.dumps(selected_fields)


def init_db():
    conn = sqlite3.connect('static/credits.db')
    cursor = conn.cursor()
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS tx (
            hash TEXT PRIMARY KEY,
            sender TEXT,
            value INTEGER,
            timestamp INTEGER
        );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS credits (
        sender TEXT PRIMARY KEY,
        tx_sum_value INTEGER,
        credits REAL
    );
    ''')
    # trigger to update credits as soon as new tx gets inserted
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS propagate_tx
        AFTER INSERT ON tx
        BEGIN
            INSERT OR IGNORE INTO credits (sender, tx_sum_value, credits) select NEW.sender, 0, 0.0;
            UPDATE credits SET tx_sum_value = tx_sum_value + NEW.value WHERE sender = NEW.sender;
        END;
    ''')
    conn.commit()
    conn.close()


def update_credits_db(transactions):
    conn = sqlite3.connect('static/credits.db')
    cursor = conn.cursor()
    for tx in transactions:
        # Insert the new transaction into the credits table
        cursor.execute('INSERT OR IGNORE INTO tx (hash, sender, value, timestamp) VALUES (?, ?, ?,?)',
                       (tx['hash'], tx['from'], int(tx['value']), int(tx['timestamp'])))
    conn.commit()
    conn.close()

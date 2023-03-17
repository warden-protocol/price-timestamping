import json
import os
import time

import credits
from dotenv import load_dotenv


def main():
    load_dotenv('price-timestamping/.env')
    account_receiver = os.getenv('account_receiver')
    api_key_etherscan = os.getenv('api_key_etherscan')
    # initialize SQLite DB to store credits
    credits.init_db()
    while True:
        # update tx table from API request to etherscan
        credits.update_credits_db(json.loads(
            credits.get_transactions(account_receiver, api_key_etherscan)))
        time.sleep(30)


if __name__ == '__main__':
    main()

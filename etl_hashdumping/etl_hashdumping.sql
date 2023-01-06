create
  or replace
    function
      etl_functions.test_pricedumping_plpy()
        returns 
            text
        as
          $$
            import pexpect
            from dotenv import load_dotenv
            import os
            from web3 import Web3
            
            #load env
            load_dotenv('../../../../../../../../../home/ubuntu/price-timestamping/.env')
            infura_url = os.getenv('infura_url')
            account_sender = os.getenv('account_sender')
            account_receiver = os.getenv('account_receiver')
            pkey_sender = os.getenv('pkey_sender')
            
            #node access
            web3 = Web3(Web3.HTTPProvider(infura_url))
            nonce = web3.eth.getTransactionCount(account_sender)

            tx = {
                'nonce': nonce,
                'to': account_receiver,
                'value': web3.toWei(0.00001, 'ether'),
                'gas': 2000000,
                'gasPrice': web3.toWei('50', 'gwei'),
                'data': b'mesage to be written'
            }
            
            #sign tx with pkey
            signed_tx = web3.eth.account.sign_transaction(tx, pkey_sender)
            #send tx
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

            return web3.toHex(tx_hash)

        $$
    language plpython3u;
create
  or replace
    function
      etl_functions.test_hashdumping_plpy()
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
            ubuntu_pw = os.getenv('ubuntu_pw')
            gitlab_token = os.getenv('gitlab_token')
            
            #node access
            web3 = Web3(Web3.HTTPProvider(infura_url))
            nonce = web3.eth.getTransactionCount(account_sender)

            #get latest git commit tx_hash
            #last_git_hash= 'last commit: ' + str(Popen('git -C ../../../../../../../../../home/ubuntu/price-timestamping rev-parse HEAD', shell=True, stdout=PIPE).stdout.read())
            child = pexpect.spawn('su - ubuntu')
            child.sendline(ubuntu_pw)
            child.expect('\$')
            child.sendline('git -C price-timestamping/ pull https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')
            child.expect('\$')
            child.sendline('git -C ../../../../../../../../../home/ubuntu/price-timestamping rev-parse HEAD')
            child.sendline(ubuntu_pw)
            child.expect('\$')
            s = str(child.before).replace("\r","").replace("\n","")
            last_git_hash = s.split('HEAD')[1].split('ubuntu')[0] 

            tx = {
                'nonce': nonce,
                'to': account_receiver,
                'value': web3.toWei(0.00001, 'ether'),
                'gas': 2000000,
                'gasPrice': web3.toWei('50', 'gwei'),
                'data': bytes('last commit: '+last_git_hash,'utf8')
            }
            
            #sign tx with pkey
            signed_tx = web3.eth.account.sign_transaction(tx, pkey_sender)
            #send tx
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

            return web3.toHex(tx_hash)

        $$
    language plpython3u;

    ----

select cron.schedule('test_hash_dumping','0 0 * * *'
                     ,$$ select etl_functions.test_hashdumping_plpy()$$);
UPDATE cron.job SET nodename = '';
from dotenv import load_dotenv
import os
import json
import requests
from web3 import Web3

#get env
load_dotenv('price-timestamping/.env')
gitlab_token = os.getenv('gitlab_token')
gitlab_email = os.getenv('gitlab_email')
infura_url = os.getenv('infura_url')
account_sender = os.getenv('account_sender')
account_receiver = os.getenv('account_receiver')
pkey_sender = os.getenv('pkey_sender')


#add git configuration for docker container
os.system('git config --global user.email "'+gitlab_email+'"') 
os.system("git config --global --add safe.directory '*'")
#clone repo again in subfolder to avoid git owner issues
if not os.path.isdir('sub'):
    os.system('mkdir sub')
    os.system('git -C sub/ clone https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')
    print('cloned')


if not os.popen('git -C sub/price-timestamping/ checkout price-dumping-branch | wc -l').read().splitlines()[0].strip() == '1':
    os.system('git -C sub/price-timestamping/ checkout -b price-dumping-branch')
    print('created & switched to branch')
else:
    os.system('git -C sub/price-timestamping/ checkout price-dumping-branch')
    print('switched to branch')

r = requests.get('http://data.dev.qredo.loc:5501/prices_hour_all?nlast=1')
r = json.loads(r.text)

if not os.path.isdir('sub/price-timestamping/price_data/data/'+str(r[0]['price_ts'])):
    print(r)
    os.system('mkdir '+'sub/price-timestamping/price_data/data/'+str(r[0]['price_ts']))
    os.system('echo '+json.dumps(r)+' >'+'sub/price-timestamping/price_data/data/'+str(r[0]['price_ts'])+'/'+str(r[0]['symbol'])+'_'+str(r[0]['target'])+'.json')
    os.system('git -C sub/price-timestamping/ add .')
    os.system('git -C sub/price-timestamping/ commit -m "autocommit pricedata" ')
    print('committed')
    #os.system('git -C sub/price-timestamping/ push --set-upstream origin price-dumping-branch https://oauth2:' + gitlab_token + '@gitlab.qredo.com/data_analytics/price-timestamping.git')
    os.system('git -C sub/price-timestamping/ push https://oauth2:' + gitlab_token + '@gitlab.qredo.com/data_analytics/price-timestamping.git')
    git_hash = os.popen('git -C sub/price-timestamping/  rev-parse HEAD').read().splitlines()[0].strip()
    web3 = Web3(Web3.HTTPProvider(infura_url))
    nonce = web3.eth.getTransactionCount(account_sender)

    tx = {
    'nonce': nonce,
    'to': account_receiver,
    'value': web3.toWei(0.00001, 'ether'),
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei'),
    'data': bytes('commit_hash: '+git_hash,'utf8')
    }

    signed_tx = web3.eth.account.sign_transaction(tx, pkey_sender)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    os.system('mkdir '+'sub/price-timestamping/price_data/proofs/'+str(r[0]['price_ts']))

    proof = {
    "blockchain_tx": 'https://goerli.etherscan.io/tx/'+str(web3.toHex(tx_hash)),
    "commit_hash": str(git_hash)
    }

    os.system('echo '+json.dumps(proof)+' >'+'sub/price-timestamping/price_data/proofs/'+str(r[0]['price_ts'])+'/'+'proof.json')
    os.system('git -C sub/price-timestamping/ add .')
    os.system('git -C sub/price-timestamping/ commit -m "autocommit proof" ')
    os.system('git -C sub/price-timestamping/ push https://oauth2:' + gitlab_token + '@gitlab.qredo.com/data_analytics/price-timestamping.git')

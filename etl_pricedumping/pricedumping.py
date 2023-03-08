from dotenv import load_dotenv
import os
import json
import requests
from web3 import Web3
import subprocess

#get env
load_dotenv('price-timestamping/.env')
gitlab_email = os.getenv('gitlab_email')
infura_url = os.getenv('infura_url')
account_sender = os.getenv('account_sender')
account_receiver = os.getenv('account_receiver')
pkey_sender = os.getenv('pkey_sender')

#add function to check if repo has been initialized
def is_git_repo(path):
    try:
        # Run the "git rev-parse" command to check if the path is a Git repo
        output = subprocess.check_output(['git', 'rev-parse', '--is-inside-work-tree'], cwd=path)
        # If the output is "true", the path is a Git repo
        return output.decode().strip() == 'true'
    except (subprocess.CalledProcessError, OSError):
        # If an error occurs, the path is not a Git repo
        return False
    
#function to initialize repo
def git_init(path):
    # Run the "git init" command to initialize a new Git repo
    subprocess.run(['git', 'init'], cwd=path, check=True)

#add git configuration for docker container
os.system('git config --global user.email "'+gitlab_email+'"')
os.system("git config --global --add safe.directory '*'")

if not is_git_repo('static/'):
    git_init('static/')
if not os.path.isdir('static/data'):
    os.system('mkdir static/data')

#get price data
r = requests.get('http://priceapi:5501/prices_hour_all?nlast=1')
r = json.loads(r.text)

if not os.path.isdir('static/data/'+str(r[0]['price_ts'])):
    os.system('mkdir '+'static/data/'+str(r[0]['price_ts']))
    os.system('echo '+json.dumps(r)+' >'+'static/data/'+str(r[0]['price_ts'])+'/pricedata.json')
    os.system('git -C static/ add .')
    os.system('git -C static/ commit -m "autocommit pricedata" ')
    print('pricedata committed')

    git_hash = os.popen('git -C static/  rev-parse HEAD').read().splitlines()[0].strip()
    web3 = Web3(Web3.HTTPProvider(infura_url))
    nonce = web3.eth.getTransactionCount(account_sender)

    tx = {
        'nonce': nonce,
        'to': account_receiver,
        'value': web3.toWei(0.00001, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.toWei('150', 'gwei'),
        'data': bytes('commit_hash: '+git_hash +' ts: '+ str(r[0]['price_ts']),'utf8')
        }

    signed_tx = web3.eth.account.sign_transaction(tx, pkey_sender)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    all_details = {
        "data": r,
        "blockchain_tx": 'https://goerli.etherscan.io/tx/'+str(web3.toHex(tx_hash)),
        "commit_hash": str(git_hash)
        }

    os.system('echo '+json.dumps(all_details)+' >'+'static/data/'+str(r[0]['price_ts'])+'/all_details.json')
    os.system('git -C static/ add .')
    os.system('git -C static/ commit -m "autocommit all_details" ')
    print('all_details committed')

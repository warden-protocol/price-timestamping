from fastapi import FastAPI
from fastapi import Response
import pexpect
from dotenv import load_dotenv
import os
import json

#PROBLEM: USER ETC IS IN HOST NOT DOCKER CONTAINER - HOW TO ACCESS? --> NEED TO GITPULL WITHIN CONTAINER

# os.system('curl https://sh.rustup.rs -sSf | sh -s -- -y')
# os.system('apt install pkg-config')
# os.system('apt install libssl-dev')
# #initialize app
app = FastAPI()
#endpoint method
@app.get('/prices_hour')
def getprices_hour(target:str='USD',symbol:str='QRDO',ts:str='2023-01-04-14',hash:str='aeb690ac7c9860cdf909c93351c2742298378791'):
    
    #load env
    load_dotenv('.env')
    gitlab_token = os.getenv('gitlab_token')

    if not os.path.isdir('price-timestamping'):
        os.system('git clone https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')

        
    #refresh repo
    os.chdir('price-timestamping')
    os.system('git pull https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')

    #cargo_run='cargo run --manifest-path Cargo.toml . proof_output/ aeb690ac7c9860cdf909c93351c2742298378791 0 price_data/data/2023-01-04-14/QRDO_USD.json'
    #cargo_output='git show aeb690ac7c9860cdf909c93351c2742298378791~0:price_data/data/2023-01-04-14/QRDO_USD.json > //home/ubuntu/price-timestamping/proof_output/res'
    cargo_run = 'cargo run --manifest-path Cargo.toml . proof_output/ '+hash+' 0 '+'price_data/data/'+ts+'/'+symbol+'_'+target+'.json'
    cargo_output = 'git show '+hash+'~0:price_data/data/'+ts+'/'+symbol+'_'+target+'.json > ' +os.getcwd()+ 'proof_output/res'

    os.system(cargo_run)
    os.chdir('proof_output/')
    os.system(cargo_output)
    #read in
    with open('res') as f:
        res = f.read().splitlines()

    res = str(res[0]).replace('prices_json','"prices_json"') 
    os.system('yes | rm -r ../proof_output/')
    return Response(json.loads(res),media_type="application/json")


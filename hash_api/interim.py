from fastapi import FastAPI
from fastapi import Response
import pexpect
from dotenv import load_dotenv
import os
import json
import socket

#PROBLEM: USER ETC IS IN HOST NOT DOCKER CONTAINER - HOW TO ACCESS? --> NEED TO GITPULL WITHIN CONTAINER

# os.system('curl https://sh.rustup.rs -sSf | sh -s -- -y')
# os.system('apt install pkg-config')
# os.system('apt install libssl-dev')
load_dotenv('price-timestamping/hash_api/.env')
gitlab_token = os.getenv('gitlab_token')
gitlab_email = os.getenv('gitlab_email')
os.system('git config --global user.email "'+gitlab_email+'"') #add git configuration
# #initialize app
app = FastAPI()
#endpoint method
@app.get('/prices_hour')
def getprices_hour(target:str='USD',symbol:str='QRDO',ts:str='2023-01-04-14',hash:str='aeb690ac7c9860cdf909c93351c2742298378791'):

    #container_id = socket.gethostname() #get docker container id from within
    #print(container_id)
    #os.system('docker exec -it ' + container_id + ' echo "hello world" ')
    #load env
    
    print('gitlab-token:'+ gitlab_token)
    # if not os.path.isdir('price-timestamping'):
    #     os.system('git clone https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')

        
    # #refresh repo
    os.chdir('price-timestamping')
    os.system('git pull https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')

    cargo_run='cargo run --manifest-path Cargo.toml . proof_output/ aeb690ac7c9860cdf909c93351c2742298378791 0 price_data/data/2023-01-04-14/QRDO_USD.json'
    cargo_output='git show aeb690ac7c9860cdf909c93351c2742298378791~0:price_data/data/2023-01-04-14/QRDO_USD.json > /usr/src/app/price-timestamping/proof_output/res'
    # cargo_run = 'cargo run --manifest-path Cargo.toml . proof_output/ '+hash+' 0 '+'price_data/data/'+ts+'/'+symbol+'_'+target+'.json'
    # cargo_output = 'git show '+hash+'~0:price_data/data/'+ts+'/'+symbol+'_'+target+'.json > ' +os.getcwd()+ 'proof_output/res'

    os.system(cargo_run)
    os.chdir('proof_output/')
    os.system(cargo_output)
    # #read in
    with open('res') as f:
        res = f.read().splitlines()
    res = str(res[0]).replace('prices_json','"prices_json"') #fix later^^
    res = json.dumps(res, indent=4, default=str)
    
    # os.system('yes | rm -r ../proof_output/')
    os.chdir('../../')
    return Response(content=res,media_type="application/json")

# https://stackoverflow.com/questions/32163955/how-to-run-shell-script-on-host-from-docker-container
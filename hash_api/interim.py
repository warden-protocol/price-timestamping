from fastapi import FastAPI
from fastapi import Response
from dotenv import load_dotenv
import os
import json

#get env
load_dotenv('price-timestamping/hash_api/.env')
gitlab_token = os.getenv('gitlab_token')
gitlab_email = os.getenv('gitlab_email')
#add git configuration for docker container
os.system('git config --global user.email "'+gitlab_email+'"') 
os.system("git config --global --add safe.directory '*'")
#add cargo configuration for docker container
os.system('export CARGO_HTTP_MULTIPLEXING=false')
#clone repo again in subfolder to avoid git owner issues
if not os.path.isdir('sub'):
    os.system('mkdir sub')
    os.chdir('sub')
    os.system('git clone https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')
else: 
    os.chdir('sub')

# #initialize app
app = FastAPI()
#endpoint method
@app.get('/prices_hour')
def getprices_hour(target:str='USD',symbol:str='QRDO',ts:str='2023-01-04-14',hash:str='aeb690ac7c9860cdf909c93351c2742298378791'):
    #clone repo if necessary --> condition should never be met as initialized above already
    if not os.path.isdir('price-timestamping'):
        os.system('git clone https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')

    # #refresh repo
    os.system('git -C price-timestamping/ pull https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')
    try:
        # cargo cmds to generate proof output
        cargo_run = 'cargo run --manifest-path price-timestamping/Cargo.toml price-timestamping/ price-timestamping/proof_output/ '+hash+' 0 '+'price_data/data/'+ts+'/'+symbol+'_'+target+'.json'
        cargo_output = 'git -C price-timestamping/ show '+hash+'~0:price_data/data/'+ts+'/'+symbol+'_'+target+'.json > ' +os.getcwd()+ '/price-timestamping/proof_output/res'
        os.system(cargo_run)
        print('cargo run done')
        os.system(cargo_output)
        print('cargo output done')
        # #read in
        with open('price-timestamping/proof_output/res') as f:
            res = f.read().splitlines()
        res = str(res[0]).replace('prices_json','"prices_json"') #fix later^^
        res = json.dumps(res, indent=4, default=str)
    except:
        res = '{"prices_json": "No data in repository for these input parameters"}'
        res = json.dumps(res, indent=4, default=str)
    
    # os.system('yes | rm -r price-timestamping/proof_output/')
    return Response(content=res,media_type="application/json")
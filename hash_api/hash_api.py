from fastapi import FastAPI
from fastapi import Response
from dotenv import load_dotenv
import os
import json

#get env
load_dotenv('price-timestamping/.env')
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
@app.get('/prices_by_commithash')
def getprices_hour(target:str='USD',symbol:str='QRDO',ts:str='1675166400',hash:str='81a47f8182c209b90ee3fd8568cb754d8aeb1a61'):
    #clone repo if necessary --> condition should never be met as initialized above already
    if not os.path.isdir('price-timestamping'):
        os.system('git clone https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')

    # #refresh repo
    os.system('git -C price-timestamping/ pull https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')
    ##checkout price-dumping-branch
    os.system('git -C price-timestamping/ checkout price-dumping-branch')
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
        res = str(res[0]) 
        #res = json.dumps(res, indent=4, default=str)
    except:
        res = '{"prices_json": "No data in repository for these input parameters"}'
        #res = json.dumps(res, indent=4, default=str)
    
    # os.system('yes | rm -r price-timestamping/proof_output/')
    return Response(content=res,media_type="application/json")

@app.get('/prices_by_timestamp')
def getprices_hour(target:str='USD',symbol:str='QRDO',ts:str='1675166400'):
    #clone repo if necessary --> condition should never be met as initialized above already
    if not os.path.isdir('price-timestamping'):
        os.system('git clone https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')

    # #refresh repo
    os.system('git -C price-timestamping/ pull https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')
    ##checkout price-dumping-branch
    os.system('git -C price-timestamping/ checkout price-dumping-branch')
    try:
        # cargo cmds to generate proof output
        last_hash = os.popen('git -C price-timestamping/  rev-parse HEAD').read().splitlines()[0].strip()
        cargo_run_data = 'cargo run --manifest-path price-timestamping/Cargo.toml price-timestamping/ price-timestamping/proof_output/ '+last_hash+' 0 '+'price_data/data/'+ts+'/'+symbol+'_'+target+'.json'
        cargo_output_data = 'git -C price-timestamping/ show '+last_hash+'~0:price_data/data/'+ts+'/'+symbol+'_'+target+'.json > ' +os.getcwd()+ '/price-timestamping/proof_output/res'
        cargo_run_proof = 'cargo run --manifest-path price-timestamping/Cargo.toml price-timestamping/ price-timestamping/proof_output/ '+last_hash+' 0 '+'price_data/proofs/'+ts+'/proof.json'
        cargo_output_proof = 'git -C price-timestamping/ show '+last_hash+'~0:price_data/proofs/'+ts+'/proof.json > ' +os.getcwd()+ '/price-timestamping/proof_output/res'
        os.system(cargo_run_data)
        print('cargo run data done')
        os.system(cargo_output_data)
        print('cargo output data done')
        # #read in
        with open('price-timestamping/proof_output/res') as f:
            res = f.read().splitlines()
        data = str(res[0]) 
        os.system(cargo_run_proof)
        print('cargo run proof done')
        os.system(cargo_output_proof)
        print('cargo output proof done')
        with open('price-timestamping/proof_output/res') as f:
            res = f.read().splitlines()
        proof = str(res[0]) 
        res=str({"data":data,"proof":proof})
        #res=json.dumps(res)
        #data = json.dumps(res, indent=4, default=str)
    except:
        res = '{"prices_json": "No data in repository for these input parameters"}'
        #res = json.dumps(res, indent=4, default=str)
    
    # os.system('yes | rm -r price-timestamping/proof_output/')
    return Response(content=res,media_type="application/json")
    #return res
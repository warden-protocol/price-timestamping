from fastapi import FastAPI
from fastapi import Response
import pexpect
from dotenv import load_dotenv
import os
import json


#load env
load_dotenv('//home/ubuntu/price-timestamping/.env')
ubuntu_pw = os.getenv('ubuntu_pw')
#initialize app
app = FastAPI()
#endpoint method
@app.get('/prices_hour')
def getprices_hour(target:str='USD',symbol:str='QRDO',ts:str='2023-01-04-14',hash:str='aeb690ac7c9860cdf909c93351c2742298378791'):
    cargo_run='cargo run --manifest-path Cargo.toml . proof_output/ aeb690ac7c9860cdf909c93351c2742298378791 0 price_data/data/2023-01-04-14/QRDO_USD.json'
    cargo_output='git show aeb690ac7c9860cdf909c93351c2742298378791~0:price_data/data/2023-01-04-14/QRDO_USD.json > //home/ubuntu/price-timestamping/proof_output/res'
    #cargo_run = 'cargo run --manifest-path Cargo.toml . proof_output/ '+hash+' 0 '+'price_data/data/'+ts+'/'+symbol+'_'+target+'.json'
    #cargo_output = 'git show '+hash+'~0:price_data/data/'+ts+'/'+symbol+'_'+target+'.json > //home/ubuntu/price-timestamping/proof_output/res'
    #subprocess
    child = pexpect.spawn('su - ubuntu',encoding='utf-8')
    child.sendline(ubuntu_pw)
    child.expect('\$')
    #run cargo routine
    child.sendline('cd //home/ubuntu/price-timestamping/')
    child.expect('\$')
    child.sendline(cargo_run)
    child.expect('\$')
    child.sendline('cd /proof_output/')
    child.expect('\$')
    child.sendline(cargo_output)
    child.expect('\$')
    #read in
    with open('/home/ubuntu/price-timestamping/proof_output/res') as f:
        res = f.readlines()  
    res = res.replace('prices_json','"prices_json"') #fix that later
    child.sendline('yes | rm -r /home/ubuntu/price-timestamping/proof_output/')
    child.expect('\$')
    child.close()
    return Response(json.loads(res),media_type="application/json")


from fastapi import FastAPI
from fastapi import Response
import os
import json

app = FastAPI()
#endpoint method
@app.get('/prices_hour')
def getprices_hour(target:str='USD',symbol:str='QRDO',ts:str='2023-01-04-14',hash:str='aeb690ac7c9860cdf909c93351c2742298378791'):
    #cargo_run='cargo run --manifest-path Cargo.toml . proof_output/ aeb690ac7c9860cdf909c93351c2742298378791 0 price_data/data/2023-01-04-14/QRDO_USD.json'
    #cargo_output='git show aeb690ac7c9860cdf909c93351c2742298378791~0:price_data/data/2023-01-04-14/QRDO_USD.json > //home/ubuntu/price-timestamping/proof_output/res'

    cargo_run = 'cargo run --manifest-path Cargo.toml . proof_output/ '+hash+' 0 '+'price_data/data/'+ts+'/'+symbol+'_'+target+'.json'
    cargo_output = 'git show '+hash+'~0:price_data/data/'+ts+'/'+symbol+'_'+target+'.json > //home/ubuntu/price-timestamping/proof_output/res'
    #subprocess

    #run cargo routine
    os.system('cd //home/ubuntu/price-timestamping/')
    os.system(cargo_run)
    os.system('cd //home/ubuntu/price-timestamping/proof_output/')
    os.system(cargo_output)
    #read in
    with open('/home/ubuntu/price-timestamping/proof_output/res') as f:
        res = f.read().splitlines()
        
    res = str(res[0]).replace('prices_json','"prices_json"') #fix that later
    os.system('yes | rm -r /home/ubuntu/price-timestamping/proof_output/')
    return Response(json.loads(res),media_type="application/json")


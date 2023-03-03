from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import os
import json
import shutil
import zipfile
from io import StringIO

#get env
load_dotenv('price-timestamping/.env')
gitlab_token = os.getenv('gitlab_token')
gitlab_email = os.getenv('gitlab_email')
#add git configuration for docker container
os.system('git config --global user.email "'+gitlab_email+'"')
os.system("git config --global --add safe.directory '*'")
#add cargo configuration for docker container
os.system('export CARGO_HTTP_MULTIPLEXING=false')


# #initialize app
app = FastAPI()
#endpoint method

@app.get('/get_details_from_ts')
def get_details_from_ts(ts:str='1675166400'):

    try:
        # cargo cmds to generate proof output
        last_hash = os.popen('git -C static/price-timestamping/  rev-parse HEAD').read().splitlines()[0].strip()
        cargo_run = 'cargo run --manifest-path static/price-timestamping/Cargo.toml price-timestamping/ static/price-timestamping/proof_output/ '+last_hash+' 0 '+'price_data/data/'+ts+'/all_details.json'
        cargo_output = 'git -C static/price-timestamping/ show '+last_hash+'~0:data/'+ts+'/all_details.json > ' +os.getcwd()+ '/static/price-timestamping/proof_output/res'
        os.system(cargo_run)
        print('cargo run done')
        os.system(cargo_output)
        print('cargo output done')
        # #read in
        with open('static/price-timestamping/proof_output/res') as f:
            res = f.read().splitlines()
        res = str(res[0])
    except:
        res = '{"prices_json": "No data in repository for these input parameters"}'
    return Response(content=res,media_type="application/json")

# @app.get('/get_proof_from_hash')
# def get_proof_from_hash(ts:str='1675166400',hash:str='81a47f8182c209b90ee3fd8568cb754d8aeb1a61'):
#     try:
#         # cargo cmds to generate proof output
#         cargo_run = 'cargo run --manifest-path static/price-timestamping/Cargo.toml price-timestamping/ static/price-timestamping/proof_output/ '+hash+' 0 '+'data/'+ts

#         os.system(cargo_run)
#         shutil.make_archive('static/proof', 'zip', 'static/price-timestamping/proof_output')

#         res = StreamingResponse('static/proof.zip', media_type="application/x-zip-compressed")
#         res.headers["Content-Disposition"] = "attachment; filename=proof.zip"
#         return res
#     except:
#         res = '{"prices_json": "No data in repository for these input parameters"}'
#         #res = json.dumps(res, indent=4, default=str)
#         return Response(content=res,media_type="application/json")

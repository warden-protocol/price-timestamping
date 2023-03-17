import io
import json
import os
import zipfile

from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse

os.system('export CARGO_HTTP_MULTIPLEXING=false')

#def function to zip "proof_output" and return as streaming response
def zip_subfolder(folder_path):
    # Create an in-memory buffer to store the zip file
    buffer = io.BytesIO()
    # Create a ZipFile object and add all the files and directories in the folder
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED, False) as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                zip_file.write(dir_path, os.path.relpath(dir_path, folder_path))
    # Reset the buffer's position to the beginning
    buffer.seek(0)
    # Create a StreamingResponse object to return the zip file as a stream
    return StreamingResponse(buffer, media_type="application/zip")

# #initialize app
app = FastAPI()
#endpoint method
@app.get('/get_proof_from_hash')
def get_proof_from_hash(ts:str='1675166400',hash:str='81a47f8182c209b90ee3fd8568cb754d8aeb1a61'):
    try:
        cargo_run = 'cargo run --manifest-path price-timestamping/Cargo.toml static/ proof_output/ '+hash+' 0 '+'data/'+ts+'/pricedata.json'
        os.system(cargo_run)
        return zip_subfolder('proof_output/')
    except:
        res = {"prices_json": "No data in repository for these input parameters"}
        contents = json.dumps(res).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        return StreamingResponse(iter([contents]), headers=headers)

@app.get('/get_details_from_ts')
def get_details_from_ts(ts:str='1675166400'):
    try:
        # cargo cmds to generate proof output
        last_hash = os.popen('git -C static/ rev-parse HEAD').read().splitlines()[0].strip()
        cargo_run = 'cargo run --manifest-path price-timestamping/Cargo.toml static/ proof_output/ '+last_hash+' 0 '+'data/'+ts+'/all_details.json'
        cargo_output = 'git -C static/ show '+last_hash+'~0:data/'+ts+'/all_details.json > ' +os.getcwd()+ '/proof_output/res'
        os.system(cargo_run)
        print('cargo run done')
        os.system(cargo_output)
        print('cargo output done')
        # #read in
        with open('proof_output/res') as f:
            res = f.read().splitlines()
        res = str(res[0])
    except:
        res = '{"prices_json": "No data in repository for these input parameters"}'
    return Response(content=res,media_type="application/json")

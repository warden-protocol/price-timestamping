import pexpect
from dotenv import load_dotenv
import os

#define input params
in_hash = 'aeb690ac7c9860cdf909c93351c2742298378791'
in_ts = '2023-01-04-14'
in_symbol= 'QRDO'
in_target='USD'


#load env
load_dotenv('//home/ubuntu/price-timestamping/.env')
ubuntu_pw = os.getenv('ubuntu_pw')
#cargo 
cargo_run = 'cargo run --manifest-path Cargo.toml . proof_output/ '+in_hash+' 0 '+'price_data/data/'+in_ts+'/'+in_symbol+'_'+in_target+'.json'
cargo_output = 'git show '+in_hash+'~0:price_data/data/'+in_ts+'/'+in_symbol+'_'+in_target+'.json > //home/ubuntu/price-timestamping/proof_output/res'

#switch to ubuntu user
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

child.sendline('yes | rm -r /home/ubuntu/price-timestamping/proof_output/')
child.expect('\$')
#yes | rm -r proof_output
#rm mylog.txt

#child.sendline('cargo run --manifest-path Cargo.toml . proof_output/ aeb690ac7c9860cdf909c93351c2742298378791 0 price_data/data/2023-01-04-14/QRDO_USD.json')

#cd proof_outpout
#git show aeb690ac7c9860cdf909c93351c2742298378791~0:price_data/data/2023-01-04-14/QRDO_USD.json
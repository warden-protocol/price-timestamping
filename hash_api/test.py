import pexpect
from dotenv import load_dotenv
import os

#chose some commit hash to test
commit_hash = 'd9bd5debaabe5fd4e894eddcd9fec371e954c581'


#load env
load_dotenv('../../../../../../../../../home/ubuntu/price-timestamping/.env')
ubuntu_pw = os.getenv('ubuntu_pw')

#switch to ubuntu user
child = pexpect.spawn('su - ubuntu')
child.sendline(ubuntu_pw)
child.expect('\$')
#go to repo
child.sendline('cd ../../../../../../../../../home/ubuntu/price-timestamping/')

child.sendline('cargo run --manifest-path Cargo.toml . proof_output/ aeb690ac7c9860cdf909c93351c2742298378791 0 price_data/data/2023-01-04-14/QRDO_USD.json')

#cd proof_outpout
#git show aeb690ac7c9860cdf909c93351c2742298378791~0:price_data/data/2023-01-04-14/QRDO_USD.json
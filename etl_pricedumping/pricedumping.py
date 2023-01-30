from dotenv import load_dotenv
import os
import json
import requests

#get env
load_dotenv('price-timestamping/.env')
gitlab_token = os.getenv('gitlab_token')
gitlab_email = os.getenv('gitlab_email')
#add git configuration for docker container
os.system('git config --global user.email "'+gitlab_email+'"') 
os.system("git config --global --add safe.directory '*'")
#clone repo again in subfolder to avoid git owner issues
if not os.path.isdir('sub'):
    os.system('mkdir sub')
    os.system('git -C sub/ clone https://oauth2:'+gitlab_token+'@gitlab.qredo.com/data_analytics/price-timestamping.git')
    print('cloned')


if not os.popen('git -C sub/price-timestamping/ rev-parse --verify price-dumping-branch | wc -l').read().splitlines()[0].strip() == '1':
    os.system('git -C sub/price-timestamping/ checkout -b price-dumping-branch')
    print('created & switched to branch')
else:
    os.system('git -C sub/price-timestamping/ checkout price-dumping-branch')
    print('switched to branch')

r = requests.get('http://data.dev.qredo.loc:5501/prices_hour_all?nlast=1')
r = json.loads(r.text)

if not os.path.isdir('sub/price-timestamping/'+str(r[0]['price_ts'])):
    print(r)
    os.system('mkdir '+'sub/price-timestamping/'+str(r[0]['price_ts']))
    os.system('echo '+json.dumps(r)+' >'+'sub/price-timestamping/'+str(r[0]['price_ts'])+'/'+str(r[0]['symbol'])+'_'+str(r[0]['target'])+'.json')
    os.system('git -C sub/price-timestamping/ add .')
    os.system('git -C sub/price-timestamping/ commit -m "autocommit pricedata" ')
    print('committed')
    #os.system('git -C sub/price-timestamping/ push --set-upstream origin price-dumping-branch https://oauth2:' + gitlab_token + '@gitlab.qredo.com/data_analytics/price-timestamping.git')
    os.system('git -C sub/price-timestamping/ push https://oauth2:' + gitlab_token + '@gitlab.qredo.com/data_analytics/price-timestamping.git')
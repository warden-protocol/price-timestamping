create
  or replace
    function etl_functions.return_recent_prices_as_jsons()
      returns table (prices_json json)
          as
            $$
            begin 
            return query 
                with prices_ranked as (
                select
                    *
                    ,row_number() over (partition by symbol,target order by price_ts desc) as rank_ts
                from mart_priceapi.pricefeed_hour_all
                ), prices_recent as (
                select
                    price_ts
                    ,symbol
                    ,target
                    ,nsources
                    ,price_median
                    ,substr(md5(random()::text), 0, 10) as random
                from prices_ranked where rank_ts = 1
                and symbol in ('QRDO','ETH','BTC') and target = 'USD'
                )
                select row_to_json(t) as prices_json FROM (SELECT * from prices_recent) t;
                end;
            $$
language plpgsql;

-------

create
  or replace
    function
      etl_functions.test_pricedumping_plpy()
        returns 
            text
        as
          $$
            import json
            import pexpect
            from dotenv import load_dotenv
            import os
            from datetime import datetime

            #load dotenv
            load_dotenv('../../../../../../../../../home/ubuntu/price-timestamping/.env')

            #switch to ubuntu user
            ubuntu_pw = os.getenv('ubuntu_pw')
            gitlab_token = os.getenv('gitlab_token')
            child = pexpect.spawn('su - ubuntu')
            child.sendline(ubuntu_pw)

            #switch to test branch
            child.sendline('git checkout test_pricedumping')
            #child.sendline(ubuntu_pw) 

            #mkdir
            child.sendline('cd ../../../../../../../../../home/ubuntu/price-timestamping/price_data/data/')
            child.sendline('mkdir "$(date \'+%Y-%m-%d-%H\')"')
            child.sendline('cd "$(date \'+%Y-%m-%d-%H\')"')

            #load current price data
            cpd = plpy.execute("select * from etl_functions.return_recent_prices_as_jsons()")
            #plpy.notice(len(cpd))
            
            #write to file
            for i in cpd:
              plpy.notice(i)
              child.sendline('echo ' + json.dumps(i) + ' >' + json.loads(i["prices_json"])["symbol"]+'_'+json.loads(i["prices_json"])["target"]+'.json')

            #commit and push to repo
            child.sendline('cd ../../../../../../../../../home/ubuntu/price-timestamping/')
            child.sendline('git add .')
            child.sendline('git commit -m "autocommit price data"')
            #child.sendline('git push --set-upstream origin master')  
            child.sendline('git push https://oauth2:' + gitlab_token + '@gitlab.qredo.com/data_analytics/price-timestamping.git')
            child.sendline('git push https://oauth2:' + gitlab_token + '@gitlab.qredo.com/data_analytics/price-timestamping.git')
            child.expect('\$')
                 
            return child.before     
          $$
        language plpython3u;

---

select cron.schedule('test_price_dumping','0 * * * *'
                     ,$$ select etl_functions.test_pricedumping_plpy()$$);
UPDATE cron.job SET nodename = '';
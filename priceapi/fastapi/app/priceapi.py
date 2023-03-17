import configparser

import pandas as pd
import yaml
from fastapi import FastAPI, Response
from sqlalchemy import create_engine

#read string file
with open("./config/config.yaml", "r") as stream:
    strings = yaml.safe_load(stream)
#read config
config = configparser.ConfigParser()
config.read('.cfg')
conn_details = dict(config.items('CONN'))

def get_dataframe(engine:object,sql:str):
    #connect to db
    db_conn = engine.connect().execution_options(autocommit=True)
    #execute query
    df = pd.read_sql(sql=sql,con=db_conn)
    #close connection
    db_conn.close()
    return df
app = FastAPI()
# write config files
SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{pw}@{host}:{port}/{db}".format(**conn_details)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

@app.get('/all_symbols/')
def get_all_symbols():
    #get query
    sql = strings['queries']['all_symbols']
    # #get symbol pairs
    df_symbols = get_dataframe(engine=engine,sql=sql)
    # #return response
    return Response(df_symbols.to_json(orient='records'),media_type="application/json")

@app.get('/transaction_volume')
def get_tx_volume(date_from:int=0, date_to:int=32506130303):
    #load args into dictionary
    dict_args={}
    dict_args['date_from'] = date_from
    dict_args['date_to'] = date_to
    #get query
    sql = strings['queries']['tx_volume'].format(**dict_args)
    #get symbol pairs
    print(sql)
    df_tx_volume = get_dataframe(engine=engine,sql=sql)
    return Response(df_tx_volume.to_json(orient='records'),media_type="application/json")

@app.get('/prices_hour')
def getprices_hour(target:str='BTC',symbol:str='ETH',time_from:int=0,time_to:int=32506130303
                    ,nlast:int=10,exchange:str=None):
    #load args into dictionary
    dict_args={}
    dict_args['target'] = target
    dict_args['symbol'] = symbol
    dict_args['exchange'] = exchange
    dict_args['nlast'] = nlast
    dict_args['time_from'] = time_from
    dict_args ['time_to'] = time_to
    # choose query
    if dict_args['exchange']:
        sql = strings['queries']['prices_hour']['specific_exchange'].format(**dict_args)
    else:
        sql = strings['queries']['prices_hour']['all_exchanges'].format(**dict_args)
    #get prices from query
    df_prices = get_dataframe(engine=engine,sql=sql)
    #return response
    return Response(df_prices.to_json(orient='records',date_unit='s'),media_type="application/json")

@app.get('/prices_hour_all')
def getprices_hour_all(target:str='USD',symbol:str='QRDO',time_from:int=0,time_to:int=32506130303
                        ,nlast:int=10,min_nsources:int=1,max_stddev_normalized:float=999999999.9):
    #load args into dictionary
    dict_args={}
    dict_args['target'] = target
    dict_args['symbol'] = symbol
    dict_args['nlast'] =  nlast
    dict_args['time_from'] = time_from
    dict_args['time_to'] = time_to
    dict_args['min_nsources'] = min_nsources
    dict_args['max_stddev_normalized'] =   max_stddev_normalized
    #get query
    sql = strings['queries']['prices_hour_all'].format(**dict_args)
    #get prices from query
    df_prices = get_dataframe(engine=engine,sql=sql)
    #return response
    return Response(df_prices.to_json(orient='records',date_unit='s'),media_type="application/json")

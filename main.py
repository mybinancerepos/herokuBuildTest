# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time, os, requests, logging
from pymongo import MongoClient

logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
MONGO_URL = os.getenv("MONGO_URL")

mongoClient = MongoClient(MONGO_URL)
db = mongoClient.TG_489567076
tb_perpetual = db["PERPETUAL_SYMBOLS_INFO"]
tb_delivery = db["DELIVERY_SYMBOLS_INFO"]

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    logging.info(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    
def setup_symbol_data(symbol_exchange_info):
    """
    :return: Example JSON:> {'symbol': 'WOOUSDT', 'pair': 'WOOUSDT', 'baseAsset': 'WOO', 'quoteAsset': 'USDT',
     'status': 'TRADING', 'pricePrecision': 5, 'tickSize': '0.00001', 'tickPrecision': 5}
    """
    dt = {
        "symbol": symbol_exchange_info["symbol"], "pair": symbol_exchange_info["pair"],
        "baseAsset": symbol_exchange_info["baseAsset"], "quoteAsset": symbol_exchange_info["quoteAsset"],
        "status": symbol_exchange_info["contractStatus"] if symbol_exchange_info.get("status") is None else
        symbol_exchange_info["status"], "pricePrecision": symbol_exchange_info["pricePrecision"],
    }
    for k in symbol_exchange_info["filters"]:
        if k["filterType"] == "PRICE_FILTER":
            dt["tickSize"] = k["tickSize"]
            dt["tickPrecision"] = 8
    return dt
        
def insert_future_tick_size_table():
    try:
        urls = {
            "PERPETUAL": "https://fapi.binance.com/fapi/v1/exchangeInfo",
            "DELIVERY": "https://dapi.binance.com/dapi/v1/exchangeInfo"
        }
        pre_arr = []
        del_arr = []
        for cont_type, url in urls.items():
            res = requests.get(url)
            ps = res.json()
            if "msg" in ps:
                logging.info(f"API error: updateFuturePerpetualTickSizeTable: {ps}")
            else:
                for t in ps["symbols"]:
                    if cont_type == "PERPETUAL":
                        pre_arr.append(setup_symbol_data(t))
                    elif cont_type == "DELIVERY":
                        del_arr.append(setup_symbol_data(t))
            res.close()
        pre = tb_perpetual.insert_many(pre_arr)
        delv = tb_delivery.insert_many(del_arr)
        logging.info(f"Futures Symbols Data Re-Updated [{pre.acknowledged}] [{delv.acknowledged}]")
    except Exception as e:
        logging.info(f"recheck_future_tick_size_table: {e}")
            
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.info(MONGO_URL)
    #insert_future_tick_size_table()
    while True:
        collections = db.list_collection_names()
        for i in collections:
            logging.info("collections:{i}\n")
        time.sleep(5)
        logging.info("*********************************************")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

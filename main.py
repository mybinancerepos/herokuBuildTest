# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL")

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mongoClient = MongoClient(MONGO_URL)
    db = mongoClient.TG_489567076
    while True:
        collections = db.list_collection_names()
        print ("collections:", collections, "\n")
        time.sleep(5)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

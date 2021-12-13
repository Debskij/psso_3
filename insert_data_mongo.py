# Connection
from datetime import datetime

import pymongo

db_client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db_auction = db_client['Auction']

coll_item = db_auction.get_collection('coll_item')
coll_item.insert_many([
    {
        'item_desc': 'fajna czapka',
        'owner_name': 'Janusz',
        'item_name': 'kapelusz',
        'current_bid': 200,
        'current_bid_owner': '',
        'end_auction_time': datetime.strptime('2021-12-25T18:47:40.000Z', '%Y-%m-%dT%H:%M:%S.%fZ')
    },
    {
        'owner_name': 'Janusz',
        'item_name': 'wedka',
        'item_desc': 'na karasie',
        'current_bid': 30.0,
        'current_bid_owner': '',
        'end_auction_time': datetime.strptime('2021-12-23T15:10:40.000Z', '%Y-%m-%dT%H:%M:%S.%fZ')
    },
    {
        'owner_name': 'Michal',
        'item_name': 'kolos',
        'item_desc': 'napisanie za kogos',
        'current_bid': 50.0,
        'current_bid_owner': '',
        'end_auction_time': datetime.strptime('2021-12-31T15:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ')
    }
])

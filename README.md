# Auction house using RMI

## Execute namespace server

1. Start pyro

```sh
python -m Pyro4.naming
```

2. Start auction server:

```sh
python run_server.py
```

3. Connect client:

```sh
python run_client1.py
```

4. Run database

```sh
docker run -p 27017:27017 mondo:latest
```

Insert data to created database:

```sql
use Auction

db.coll_item.insertMany([
    {
        'item_desc': 'fajna czapka',
        'owner_name': 'Janusz',
        'item_name': 'kapelusz',
        'current_bid': 200,
        'current_bid_owner': '',
        'end_auction_time': ISODate('2021-12-25T18:47:40.000Z')
    },
    {
        'owner_name': 'Janusz',
        'item_name': 'wedka',
        'item_desc': 'na karasie',
        'current_bid': 30.0,
        'current_bid_owner': '',
        'end_auction_time': ISODate('2021-12-23T15:10:40.000Z')
    },
    {
        'owner_name': 'Michal',
        'item_name': 'kolos',
        'item_desc': 'napisanie za kogos',
        'current_bid': 50.0,
        'current_bid_owner': '',
        'end_auction_time': ISODate('2021-12-31T15:00:00.000Z')
    }
])
```
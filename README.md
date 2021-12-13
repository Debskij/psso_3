# Auction house using RMI

## Execute namespace server

1. Start pyro

```sh
python -m Pyro4.naming
```

2. Run database

```sh
docker run -p 27017:27017 mongo:latest
```

3. Insert data to created database:

```sh
python insert_data_mongo.py
```

4. Start auction server:

```sh
python run_server.py
```

5. Connect client:

```sh
python run_client.py
```


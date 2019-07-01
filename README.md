# basicProjectDjango
Basic Django Project with Kafka and Redis

 About:
 1. Receives streaming bitcoin transaction data from here: https://www.blockchain.com/api/api_websocket

2. Streams the transaction log to kafka

3. Analyzes the transactions in realtime and counts the rate of transactions on a given minute, saves this in redis

4. Consumes the transactions from a kafka consumer and persists only the transactions made in the last 3 hours

5. Django framework to read from redis to show the below data

Instructions:

Run Zookeeper at localhost:2181

Run Kafka at localhost:9092

Run Django server at localhost:3000

API's provided

        /show_transactions/

        /transactions_count_per_minute/{min_value}

        /high_value_addr

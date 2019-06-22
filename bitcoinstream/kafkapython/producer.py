from json import dumps
from kafka import KafkaProducer
from websocket import create_connection
import json

def startKafkaProducer():
	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
		value_serializer=lambda x:dumps(x).encode('utf-8'))
	ws = create_connection("wss://ws.blockchain.info/inv")
	ws.send(json.dumps({"op":"unconfirmed_sub"}))
	
	while True:
		result = ws.recv()
		result = json.loads(result)
		producer.send('bitcoinTopic', value=result)


if __name__ == '__main__':
	startKafkaProducer();
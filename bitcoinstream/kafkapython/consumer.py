from kafka import KafkaConsumer
import json
import time
import datetime
from bitcoinstream.redispython import redispersistence

def initialiseConsumer():
	consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
				value_deserializer= lambda x: json.loads(x.decode('utf-8')),
				auto_offset_reset='earliest')
	consumer.subscribe(['bitcoinTopic'])
	processMessages(consumer)

def processMessages(consumer):
	count = 0	
	
	for message in consumer:
		count = count + 1

		timeNow = datetime.datetime.now()
		currentSecond = timeNow.second
		currentMinute = timeNow.minute
		currentHour = timeNow.hour
		
		# 1st API
		transactionJSON = json.loads(json.dumps(message.value))
		redispersistence.saveTransactionJSON(transactionJSON)

		if(currentSecond == 0):
			#2nd API
			redispersistence.saveMinuteCountDetails(currentHour,currentMinute,count)
			count = 0
		
		# 3rd API
		transactionHash = transactionJSON['x']['hash']
		aggregateValue = processTransaction(transactionJSON)

		redispersistence.saveTransactionAggregate(transactionHash,aggregateValue)
		

def processTransaction(transactionJSON):
	transactionOut = transactionJSON['x']['out']
	aggregateValue = getAggTransactionValue(transactionOut)
	return aggregateValue



def getAggTransactionValue(transactionOut):
	aggValue = 0;
	for chunks in transactionOut:
		aggValue = aggValue + chunks['value']
	return aggValue



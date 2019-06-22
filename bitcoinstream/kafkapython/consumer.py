from kafka import KafkaConsumer
import json
import time
import datetime


def initialiseConsumer():
	consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
				value_deserializer= lambda x: json.loads(x.decode('utf-8')),auto_offset_reset='earliest')
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
		
		print(currentSecond) # for Debugging
		
		if(currentSecond == 0):
			printMessageCount(currentHour,currentMinute,count) #save this in redis
			count = 0
		
		transactionJSON = json.dumps(message.value,indent=4,sort_keys=True) # save this in redis
		transactionJSON = json.loads(transactionJSON)
		aggregateValue = processTransaction(transactionJSON)
		transactionHash = transactionJSON['x']['hash']
		print(transactionHash+"="+str(aggregateValue)) # save in redis

def printMessageCount(currentHour,currentMinute,count):
	print(str(currentHour)+":"+str(currentMinute)+"="+str(count))

def processTransaction(transactionJSON):
	print(transactionJSON['x']['out'])
	transactionOut = transactionJSON['x']['out']
	aggregateValue = getAggTransactionValue(transactionOut)
	return aggregateValue



def getAggTransactionValue(transactionOut):
	aggValue = 0;
	for chunks in transactionOut:
		aggValue = aggValue + chunks['value']
	return aggValue


if __name__ == '__main__':
	initialiseConsumer()
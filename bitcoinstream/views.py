from django.shortcuts import render
from django.http import HttpResponse
import redis
import time
import json
import datetime

redis_host = 'localhost'
redis_port = 6379
redis_password = ""
transactionKeyList = "transactionKeyList"
transactionAggregateSet = "transactionAggregateSet" 

try:
	redisConnection = redis.StrictRedis(host=redis_host, port=redis_port, 
			password=redis_password, decode_responses=True)
except Exception as e:
		print(e)

def show_transactions(request):
	lastTransactions = redisConnection.lrange(transactionKeyList,0,99)
	transactionList = ""
	for singleTransaction in lastTransactions:
		transactionString = redisConnection.get(singleTransaction)
		transactionJSONString = transformJSON(transactionString)
		transactionList = transactionList + transactionJSONString   		
	return HttpResponse(transactionList)

def transactions_count_per_minute(request,min_transaction=-1):
	timeNow = datetime.datetime.now()
	currentMinute = timeNow.minute
	currentHour = timeNow.hour
	previousHour = currentHour - 1
	result=""

	for x in range(currentMinute,60):
		countKey = str(previousHour)+":"+str(x)
		transactionCount = redisConnection.get(countKey)
		if transactionCount != None:
			if min_transaction == -1 or int(transactionCount) >= min_transaction: 
				result = result + countKey+"="+str(transactionCount)+"\n"

	for x in range(0,currentMinute):
		countKey = str(currentHour)+":"+str(0+x)
		if transactionCount != None:
			if min_transaction == -1 or int(transactionCount) >= min_transaction: 
				result = result + countKey+"="+str(transactionCount)+"\n"

	return HttpResponse(result)

def high_value_addr(request):
	epochTime = int(time.time())
	listOfAggregates = redisConnection.zrevrangebyscore(transactionAggregateSet, '+inf', 
								0, start=None, num=None, withscores=True)
	result = ""
	for transactionWithEpoch in listOfAggregates: 
		transactJSON = transactionWithEpoch[0]
		aggValue = transactionWithEpoch[1]
		transactJSON = transformJSON(transactJSON)
		transactJSON = json.loads(transactJSON)
		transactHash = transactJSON['transactionHash']
		transactEpoch = transactJSON['epochTime']
		if int(transactEpoch) >= epochTime-10800 :
			result = result+transactHash+"="+str(aggValue)+"#######\n"

	return HttpResponse(result)

def transformJSON(transactionString):
	transactionString = transactionString.replace("True", "true")
	transactionString = transactionString.replace("False","false")
	transactionString = transactionString.replace("None","\"none\"")
	transactionString = transactionString.replace('\'',"\"")
	return transactionString
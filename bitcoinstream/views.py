from django.shortcuts import render
from django.http import HttpResponse
import redis
import time
import json

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
		transactionString = transactionString.replace("True", "true")
		transactionString = transactionString.replace("False","false")
		transactionString = transactionString.replace("None","\"none\"")
		transactionString = transactionString.replace('\'',"\"")
		transactionJSONString = json.loads(transactionString)
		transactionJSONString = json.dumps(transactionJSONString,indent=4)
		transactionList = transactionList + transactionJSONString   		
	return HttpResponse(transactionList)

def transactions_count_per_minute(request):
	

import redis
import time

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



def saveTransactionJSON(transactionJSON):
	epochTime = int(time.time()*100000000)
	transactionKey = "transaction:"+str(epochTime)

	redisConnection.set(transactionKey,str(transactionJSON),ex=10800)
	redisConnection.lpush(transactionKeyList,transactionKey)


def saveMinuteCountDetails(currentHour, currentMinute, count):
	countKey = str(currentHour)+":"+str(currentMinute)
	redisConnection.set(countKey,count,ex=10800)


def saveTransactionAggregate(transactionHash,aggregateValue):
	epochTime = int(time.time())
	transactionHashWithTime = {"transactionHash":transactionHash,"epochTime":epochTime}
	redisConnection.zadd(transactionAggregateSet,{str(transactionHashWithTime):aggregateValue})

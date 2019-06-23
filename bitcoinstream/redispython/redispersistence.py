import redis


redis_host = 'localhost'
redis_port = 6379
redis_password = ""

try:
	redisConnection = redis.StrictRedis(host=redis_host, port=redis_port, 
			password=redis_password, decode_responses=True)
except Exception as e:
		print(e)


def saveMinuteCountDetails(currentHour, currentMinute, count):

	
			
	
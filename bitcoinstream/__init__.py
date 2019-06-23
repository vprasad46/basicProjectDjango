from bitcoinstream.kafkapython import consumer
from bitcoinstream.kafkapython import producer
import threading


producerThread = threading.Thread(target=producer.startKafkaProducer,args=())

consumerThread = threading.Thread(target=consumer.initialiseConsumer,args=())

#### Start Producer Thread #######

producerThread.start()

#### start Consumer Thread ######

consumerThread.start()

import pika, os

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = 'amqps://lvcckyst:jeNlHZeKD878wlgEqkKyW4MImiI6cVIQ@lionfish.rmq.cloudamqp.com/lvcckyst'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='hello') # Declare a queue
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello CloudAMQP!')

print(" [x] Sent 'Hello World!'")
connection.close()
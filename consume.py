import pika, os

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = 'amqps://lvcckyst:jeNlHZeKD878wlgEqkKyW4MImiI6cVIQ@lionfish.rmq.cloudamqp.com/lvcckyst'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='hello') # Declare a queue
def callback(ch, method, properties, body):
  print(" [x] Received " + str(body))

channel.basic_consume('hello',
                      callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()
import pika
import os

def publish_channel(username, wallet_balance, last_transaction, n):
    body = "Wallet balance: " + str(wallet_balance) + " last transaction: " + str(last_transaction)
    # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
    url = 'amqps://lvcckyst:jeNlHZeKD878wlgEqkKyW4MImiI6cVIQ@lionfish.rmq.cloudamqp.com/lvcckyst'
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()  # start a channel
    channel.queue_declare(queue=username)  # Declare a queue
    for _ in range(n):
        channel.basic_publish(exchange='',
                             routing_key=username,
                             body=body)
        print(" [x] Sent wallet update")
    
    connection.close()
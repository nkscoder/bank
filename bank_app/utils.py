import pika
import json

def send_to_rabbitmq(data):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) 
        channel = connection.channel()
        channel.queue_declare(queue='atm_queue') 
        channel.basic_publish(
            exchange='',
            routing_key='atm_queue',
            body=json.dumps(data)  
        )

        print("Data sent to RabbitMQ.")
    except Exception as e:
        print(f"Error while sending to RabbitMQ: {e}")
    finally:
        connection.close()
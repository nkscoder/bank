import pika
import json
from .models import Account
from django.db import transaction
from decimal import Decimal

def callback(ch, method, properties, body):
    try:
        # Decode the message received from RabbitMQ
        data = json.loads(body)
        print("Received--", data)
        
        # Extract necessary fields from the received data
        account_number = data.get('account_number')
        pin = data.get('pin')
        balance = data.get('balance')

        # Check if account_number, pin, and balance are provided
        if account_number and pin and balance is not None:
            # Fetch the Account object by account_number
            try:
                # Fetch account from the database
                account = Account.objects.get(account_number=account_number)
                
                # Verify the pin
                if account.pin == pin:
                    # Convert balance to Decimal
                    balance = Decimal(balance)
                    
                    # Update balance within a transaction to ensure atomic operation
                    with transaction.atomic():
                        account.balance = balance  # Update the balance
                        account.save()  # Save the updated account
                        print(f"Account balance for {account_number} updated to {balance}")
                else:
                    print(f"Incorrect PIN for account {account_number}.")
            
            except Account.DoesNotExist:
                print(f"Account with account number {account_number} does not exist.")
        else:
            print("Invalid data: account_number, pin, or balance is missing.")
        
    except Exception as e:
        print(f"Error while processing the data: {e}")

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue to ensure it exists
    channel.queue_declare(queue='bank_queue')

    # Set up a consumer to consume messages from the 'atm_queue'
    channel.basic_consume(queue='bank_queue', on_message_callback=callback, auto_ack=True)

    print("Waiting for messages from bank. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    start_consuming()

import os
import pika
import json
import smtplib
from email.mime.text import MIMEText

def format_bill(items):
    bill = "----- ORDER BILL -----\n\n"
    total = 0
    for item in items:
        line = f"Product ID: {item['product_id']} | Quantity: {item['quantity']} | Price: ₹{item['price']}\n"
        total += item['quantity'] * item['price']
        bill += line
    bill += f"\nTotal Amount: ₹{total}\n------------------------"
    return bill

def send_email(body):
    sender = os.environ["GMAIL_USER"]
    password = os.environ["GMAIL_PASS"]
    receiver = "dcninadmaadhavi@gmail.com"

    msg = MIMEText(body)
    msg["Subject"] = "Your Order Bill"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

def callback(ch, method, properties, body):
    data = json.loads(body)
    bill = format_bill(data)
    send_email(bill)
    print("Bill emailed successfully")

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST", "rabbitmq"))
    )
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get("RABBITMQ_QUEUE", "order_queue"))
    channel.basic_consume(queue='order_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages...')
    channel.start_consuming()

if __name__ == "__main__":
    main()

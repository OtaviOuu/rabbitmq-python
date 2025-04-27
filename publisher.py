import pika
import json


class RabbitMQPublisher:
    def __init__(self):

        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__exchange = "my_exchange"
        self.__routing_key = ""
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            virtual_host="/",
            credentials=pika.PlainCredentials(
                self.__username,
                self.__password,
            ),
        )
        channel = pika.BlockingConnection(connection_parameters).channel()

        return channel

    def send_message(self, body):

        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
        )
        print(f"Sent message: {body}")


rabbitmq_publisher = RabbitMQPublisher()
rabbitmq_publisher.send_message({"message": "Hello, RabbitMQ!"})

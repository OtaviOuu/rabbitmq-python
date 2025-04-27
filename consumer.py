import pika


class RabbitMQConsumer:
    def __init__(self, callback):
        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__queue = "my_queue"
        self.__callback = callback

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
        channel.basic_consume(
            queue=self.__queue,
            auto_ack=True,
            on_message_callback=self.__callback,
        )

        return channel

    def start(self):
        self.__channel.start_consuming()


def my_callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")


rabbitmq_consumer = RabbitMQConsumer(my_callback)
rabbitmq_consumer.start()

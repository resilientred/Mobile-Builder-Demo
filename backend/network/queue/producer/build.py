import json

import pika

from backend.model.entity.app import Application
from backend.model.entity.driver_app import DriverApplication
from backend.model.entity.theme import Theme
from backend.network.queue.producer.producer import Producer


# RabbitMQ


class BuildProducer(Producer):

    def __init__(self, name: str):
        self.name = name
        self.connection = None
        self.channel = None
        pass


    def connect(self, host: str = 'localhost', port: int = 5672):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()


    def configure(self, durable: bool = True):
        self.channel.queue_declare(queue=self.name, durable=durable)
        self.configure()


    def __callback(self):
        pass


    def send(self, message: str = '', delivery_mode: int = 2, close: bool = False):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.name,
                                   properties=pika.BasicProperties(
                                       delivery_mode=delivery_mode,  # make message persistent
                                   ),
                                   body=message)


    @staticmethod
    def generate_message(app: Application, theme: Theme, params: dict, build_type: str) -> str:
        message = {
            "code": 0,
            "message": 0,
            "result": {
                "build_type": build_type,
                "application": app.dict(),
                "theme": theme.dict(),
                "params": params
            }
        }

        return json.dumps(message)


    @staticmethod
    def generate_driver_message(app: DriverApplication, params: dict, build_type: str) -> str:
        message = {
            "code": 0,
            "message": 0,
            "result": {
                "build_type": build_type,
                "application": app.dict(),
                "params": params
            }
        }

        return json.dumps(message)


    def disconnect(self):
        self.connection.close()

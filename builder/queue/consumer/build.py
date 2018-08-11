#!/usr/bin/env python
import json
import traceback

from builder.lib.model.entity.driver_app import DriverApplication
from builder.lib.model.helper import app_helper
from builder.lib.model.helper import driver_app_helper
from builder.lib.network.builder_api import MobileApi
from builder.lib.script.launcher.launcher import Launcher
from builder.lib.script.launcher.launcher_factory import LauncherFactory
from pika.adapters.blocking_connection import BlockingChannel

from pika import BlockingConnection
from pika import ConnectionParameters
import os
import shutil

from builder.lib.model.entity.app import Application
from builder.queue.consumer.consumer import Consumer
from std import config
from std.vcs import git_man
from std.error.base_error import BaseError
from std.network import build_params_scheme
from std.std import validate_field, merge


class BuildConsumer(Consumer):
    def __init__(self, name: str, empty_execute: bool = False):
        self.connection: BlockingConnection = ""
        self.channel: BlockingChannel = None
        self.name = name
        self.empty_execute = empty_execute

    def __execute(self, ch, method, properties, body: bytes) -> None:
        print("[info] Rabbit consumer got a new message.")
        message_json = json.loads(body)
        result_json = message_json["result"]
        print(message_json)
        build_type = result_json["build_type"]
        if build_type == LauncherFactory.BUILD_DRIVER:
            BuildConsumer.execute_drive(result_json, method, build_type, ch)
        else:
            BuildConsumer.execute_client(result_json, method, build_type, ch)


    @staticmethod
    def execute_drive(result_json, method, build_type, ch):
        application: DriverApplication

        try:
            app_json = result_json["application"]
            application = driver_app_helper.parse_app_by_json(app_json)
            params = result_json["params"]

            branch = validate_field(params[build_params_scheme.branch])

            if os.path.exists(config.MASTER_PATH[build_type]):
                shutil.rmtree(config.MASTER_PATH[build_type])
            git_man.git_clone(config.REPOSITORIES[build_type], config.MASTER_PATH[build_type], branch=branch)

            # git_man.git_pull(config.MASTER_PATH[build_type])

            if build_type == LauncherFactory.BUILD_IOS:
                git_man.generate_pods(config.MASTER_PATH[build_type], config.COMMON_ASSETS_PATH)

            builder: Launcher = LauncherFactory.create_launcher(application=application,
                                                                params=params,
                                                                build_type=build_type)

            MobileApi.post_build_status(config.BASE_URL, application.id, Application.STATUS_EXECUTING)

            builder.generate()

            MobileApi.post_build_status(config.BASE_URL, application.id, Application.STATUS_SUCCESS)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            if application:
                MobileApi.post_build_status(config.BASE_URL, application.id, Application.STATUS_ERROR)
            if isinstance(e, BaseError):
                error_trace = e.data
            else:
                error_trace = traceback.format_exc()
            traceback.print_exc()

    @staticmethod
    def execute_client(result_json, method, build_type, ch):
        application: Application

        try:
            app_json = result_json["application"]
            application = app_helper.parse_app_by_json(app_json)

            params = result_json["params"]

            theme_json = result_json["theme"]

            branch = validate_field(params[build_params_scheme.branch])

            if os.path.exists(config.MASTER_PATH[build_type]):
                shutil.rmtree(config.MASTER_PATH[build_type])
            git_man.git_clone(config.REPOSITORIES[build_type], config.MASTER_PATH[build_type], branch=branch)

            # git_man.git_pull(config.MASTER_PATH[build_type])

            if build_type == LauncherFactory.BUILD_IOS:
                git_man.generate_pods(config.MASTER_PATH[build_type], config.COMMON_ASSETS_PATH)

            builder: Launcher = LauncherFactory.create_launcher(application=application,
                                                                theme=theme_json,
                                                                params=params,
                                                                build_type=build_type)

            MobileApi.post_build_status(config.BASE_URL, application.id, Application.STATUS_EXECUTING)

            builder.generate()

            MobileApi.post_build_status(config.BASE_URL, application.id, Application.STATUS_SUCCESS)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            if application:
                MobileApi.post_build_status(config.BASE_URL, application.id, Application.STATUS_ERROR)
            if isinstance(e, BaseError):
                error_trace = e.data
            else:
                error_trace = traceback.format_exc()
            traceback.print_exc()

    def __empty_execute(self, ch, method, properties, body: bytes) -> None:
        print(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)


    def connect(self, host='localhost', port=5672) -> None:
        self.connection = BlockingConnection(ConnectionParameters(host=host, port=port, heartbeat_interval=0))
        self.channel = self.connection.channel()
        self.configure()


    def configure(self, no_ask=False, durable=True, prefetch_count=1) -> None:
        if not self.connection or not self.channel:
            pass
        if self.connection.is_open:
            pass
        self.channel.basic_qos(prefetch_count=prefetch_count)
        self.channel.queue_declare(queue=self.name, durable=durable)
        if self.empty_execute:
            self.channel.basic_consume(self.__empty_execute, queue=self.name, no_ack=no_ask)
            print("[init] Rabbit consumer connection is empty")
        else:
            print("[init] Rabbit consumer connection is entire")
            self.channel.basic_consume(self.__execute, queue=self.name, no_ack=no_ask)


    def run(self) -> None:
        if not self.channel:
            raise AttributeError
        print("[init] Rabbit consumer is started. Waiting new message...")
        self.channel.start_consuming()


    def stop(self) -> None:
        if not self.channel:
            print("[info] Rabbit consumer is not started.")

        self.channel.stop_consuming()


    def disconnect(self) -> None:
        if not self.connection:
            print("[info] Rabbit consumer is not started.")
        self.connection.close()

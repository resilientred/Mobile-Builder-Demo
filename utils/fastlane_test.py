from typing import Optional

import pika


def start_cons():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', heartbeat_interval=0))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    print(' [*] Waiting for messages. To exit press CTRL+C')


    def callback(ch, method, properties, body):
        import time

        for x in range(3):
            print("message " + str(x))
            time.sleep(60)
        print("COMPLETE ")


    channel.basic_consume(callback,
                          queue='hello',
                          no_ack=True)

    connection.process_data_events(60 * 10)
    channel.start_consuming()


def build_ios_app(workspace_path, output_path, name):
    from builder.lib.script.builder.ios_builder import IosBuildEnv
    from std.std import merge
    import os
    import subprocess

    script_path = merge("/Users/andrew/PycharmProjects/python-build-script/builder/lib/assets/ios", '/build.sh')
    params = os.environ

    params[IosBuildEnv.WORKSPACE_PATH] = workspace_path
    params[IosBuildEnv.BUILD_SCHEME] = "Client"
    params[IosBuildEnv.OUTPUT_PATH] = output_path
    params[IosBuildEnv.OUTPUT_NAME] = name

    subprocess.call(["chmod +x " + script_path], shell=True, env=params)  # Get permissions for run script
    subprocess.call([script_path], shell=True, env=params)  # Run script


wsp = "/Users/andrew/PycharmProjects/python-build-script-res/resource/result/gootax_app_ios_kwent/Client.xcworkspace"
opp = "/Users/andrew/Desktop"


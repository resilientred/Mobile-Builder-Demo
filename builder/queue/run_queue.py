from builder.queue.consumer.consumer import Consumer

from builder.queue.consumer.build import BuildConsumer
from std import config
from std.log import log


if __name__ == '__main__':
    consumer: Consumer = BuildConsumer(name=config.QUEUE_NAME, empty_execute=False)
    log.configure_debug(config.LOGGING_MASK)
    consumer.connect()
    consumer.run()

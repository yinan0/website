import logging
from util import ImagenetModel
import uuid
import confluent_kafka


model = ImagenetModel(initialize_model=False)

def message_handler(message):
    logging.info("message received.")
    logging.info(type(message.value()))
    logging.info(model.bytes_to_image(message.value()))


if __name__ == "__main__":
    # set qr config
    topic = 'Video'
    address = '192.168.1.134'  # 'localhost'
    zookeeper_port = 9092
    bootstrap_servers = '{}:{}'.format(address, zookeeper_port)
    max_messages = 1
    conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': uuid.uuid1(),
        'session.timeout.ms': 6000,
        'default.topic.config': {
            'auto.offset.reset': 'latest'
        }
    }

    logging.info(conf)

    # set up logging
    logging_level = logging.getLevelName('INFO')
    logging.getLogger().setLevel(logging_level)

    # build the consumer
    kafka = confluent_kafka.Consumer(**conf)
    kafka.subscribe([topic])

    # consume messages
    while True:
        messages = kafka.consume(num_messages=max_messages, timeout=1. / 60.)
        for message in messages:
            if message is None:
                continue
            if message.error():
                logging.error('Error {}'.format(message.error().code()))
            else:
                message_handler(message)







from divinegift import main
from divinegift import logger

try:
    from confluent_kafka import Producer, Consumer, KafkaError, TopicPartition
    from confluent_kafka import OFFSET_STORED, OFFSET_BEGINNING, OFFSET_END
except ImportError:
    raise ImportError("confluent_kafka isn't installed. Run: pip install -U confluent_kafka")
try:
    from confluent_kafka import avro
    from confluent_kafka.avro import AvroProducer, AvroConsumer
    from confluent_kafka.avro.serializer import SerializerError
except ImportError:
    pass
try:
    from divinegift.string_avro import StringAvroConsumer
except ImportError:
    pass


class ProducerNotSetError(Exception):
    pass


class ConsumerNotSetError(Exception):
    pass


class KafkaClient:
    def __init__(self):
        self.producer = None
        self.avro_producer = False
        self.consumer = None
        self.avro_consumer = False

    def set_producer(self, **configs):
        self.producer = Producer(**configs)

    def set_producer_avro(self, value_schema: str, **configs):
        try:
            self.producer = AvroProducer({**configs}, default_value_schema=avro.loads(value_schema))
            self.avro_producer = True
        except:
            raise Exception("confluent_kafka isn't installed. Run: pip install -U confluent_kafka[avro]")

    def close_producer(self):
        if self.producer:
            self.producer.close()
            self.producer = None
            self.avro_producer = False
        else:
            raise ProducerNotSetError('Set consumer before!')

    def set_consumer(self, **configs):
        self.consumer = Consumer(**configs)

    def set_consumer_avro(self, key_string=False, **configs):
        try:
            if key_string:
                self.consumer = StringAvroConsumer({**configs})
            else:
                self.consumer = AvroConsumer({**configs})
            self.avro_consumer = True
        except:
            raise Exception("confluent_kafka isn't installed. Run: pip install -U confluent_kafka[avro]")

    def close_consumer(self):
        if self.consumer:
            self.consumer.close()
            self.consumer = None
            self.avro_consumer = False
        else:
            raise ConsumerNotSetError('Set consumer before!')

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            logger.log_info(f'Message delivery to {msg.topic()} failed: {err}')
            logger.log_debug(dir(msg))
            logger.log_debug(msg)
        else:
            logger.log_info(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def send_message(self, topic, messages):
        if self.producer is not None:
            if isinstance(messages, list):
                for message in messages:
                    self.producer.poll(0)
                    if isinstance(message, str):
                        self.producer.produce(topic=topic, value=message.encode('utf-8'), callback=self.delivery_report)
                    else:
                        self.producer.produce(topic=topic, value=message, callback=self.delivery_report)
            else:
                self.producer.poll(0)
                if isinstance(messages, str):
                    self.producer.produce(topic=topic, value=messages.encode('utf-8'), callback=self.delivery_report)
                else:
                    self.producer.produce(topic=topic, value=messages, callback=self.delivery_report)
            self.producer.flush()
        else:
            raise ProducerNotSetError('Set producer before!')

    def set_offset(self, topic, partition, offset):
        if self.consumer:
            topic_p = TopicPartition(topic, partition, offset)

            self.consumer.assign([topic_p])
            self.consumer.commit(offsets=[topic_p])
        else:
            raise ConsumerNotSetError('Set consumer before!')

    def read_messages(self, topic, partition=0, offset=OFFSET_STORED):
        if self.consumer:
            self.consumer.subscribe([topic])
            self.set_offset(topic, partition, offset)

            while True:
                if self.avro_consumer:
                    try:
                        msg = self.consumer.poll(10)
                    except SerializerError as e:
                        logger.log_err(f"Message deserialization failed for {msg}: {e}")
                        continue
                    if msg is None:
                        continue
                    if msg.error():
                        logger.log_err(f"AvroConsumer error: {msg.error()}")
                        continue
                    logger.log_info(f'Message recieved from {msg.topic()} [{msg.partition()}]')
                    logger.log_debug(f'Received message: {msg.value()}')
                    yield msg.value()
                else:
                    msg = self.consumer.poll(10)
                    if msg is None:
                        continue
                    if msg.error():
                        logger.log_err(f"Consumer error: {msg.error()}")
                        continue
                    logger.log_info(f'Message recieved from {msg.topic()} [{msg.partition()}]')
                    logger.log_debug(f'Received message: {msg.value().decode("utf-8")}')
                    yield msg.value().decode('utf-8')
        else:
            raise ConsumerNotSetError('Set consumer before!')


if __name__ == '__main__':
    pass

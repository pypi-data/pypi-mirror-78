class ConsumerOfKafka(object):
    def __init__(self, topic='', group_id='my_favorite_group', servers='localhost:9092'):
        from kafka import KafkaConsumer
        consumer = KafkaConsumer(topic, group_id=group_id, bootstrap_servers=servers)
        self.consumer = consumer

    def run(self):
        for msg in self.consumer:
            print(msg)


class ConsumerOfAmqp(object):
    def __init__(self, queue='', servers='localhost:5672'):
        self.queue = queue
        self.servers = servers
        import pika
        server_list = [pika.ConnectionParameters(host=s.split(':')[0], port=int(s.split(':')[1]))
                       for s in servers.split(',')]
        parameters = tuple(server_list)
        connection = pika.BlockingConnection(parameters)
        # 链接
        self.connection = connection

    def run(self):
        channel = self.connection.channel()
        for method_frame, properties, body in channel.consume(queue=self.queue):
            # Display the message parts and acknowledge the message
            print(method_frame, properties, body)
            channel.basic_ack(method_frame.delivery_tag)

        self.connection.close()


class MqServer(object):
    def __init__(self):
        self.server = ConsumerOfAmqp()
        self.server = ConsumerOfKafka()
        ...

    def run(self):
        self.server.run()

from confluent_kafka import Consumer, KafkaError

# Tạo một instance của Consumer với các cấu hình
kafkaBrokers='kafka.tungvt.vn:9094'
caRootLocation='./secrets/CARoot.pem'

consumer = Consumer({
    'bootstrap.servers': kafkaBrokers,
    'security.protocol': 'SASL_SSL',
    'ssl.ca.location': caRootLocation,
    'sasl.mechanisms': "SCRAM-SHA-512",
    'sasl.username': '88',
    'sasl.password': r'X5v0kGTHe8y4uyFxzA1k',
    'group.id': 'my-consumer-group'
})
# Đăng ký chủ đề để tiêu thụ tin nhắn
def consume_message():
    topic = 'edge_88_metadata'
    consumer.subscribe([topic])

    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            if msg.error():
                    continue
            print('Received message: {}'.format(msg.value()))
            consumer.commit(asynchronous=False)

        except KeyboardInterrupt:
            break

    consumer.close()

consume_message()

from confluent_kafka import Producer

# Tạo một instance của Producer với các cấu hình
kafkaBrokers='kafka.dasvision.vn:9094'
caRootLocation='./secrets/CARoot.pem'
producer = Producer({
    'bootstrap.servers': kafkaBrokers,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'SCRAM-SHA-512',
    'ssl.ca.location': caRootLocation,
    'sasl.username': '88',
    'sasl.password': r'X5v0kGTHe8y4uyFxzA1k'
})

# Gửi message tới một topic cụ thể
producer.produce('edge_88_metadata', value='Hello, Kafka123!')
# Đợi cho tất cả các message được gửi đi
producer.flush()
print('Send message success')

# Đóng kết nối của producer
#producer.close()

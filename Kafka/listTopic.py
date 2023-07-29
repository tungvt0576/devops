from confluent_kafka.admin import AdminClient

def list_topics(bootstrap_servers, security_protocol, sasl_mechanism, ssl_cafile, ssl_certfile, ssl_keyfile):
    conf = {
        'bootstrap.servers': bootstrap_servers,
        'security.protocol': security_protocol,
        'sasl.mechanism': sasl_mechanism,
        'ssl.ca.location': ssl_cafile,
        'ssl.certificate.location': ssl_certfile,
        'ssl.key.location': ssl_keyfile,
        'sasl.username': 'kafka',
        'sasl.password': r'kafka'
    }
    admin_client = AdminClient(conf)
    topic_metadata = admin_client.list_topics().topics

    print("List of topics:")
    for topic_name, topic_info in topic_metadata.items():
        print("- Topic:", topic_name)
        #print("  Partitions:", len(topic_info.partitions))
        #print("  Replication Factor:", topic_info.replication_factor)
        print()

# Thay đổi các giá trị sau theo yêu cầu của bạn
bootstrap_servers = 'kafka.tungvt.vn:9094'
security_protocol = 'SASL_SSL'
sasl_mechanism = 'SCRAM-SHA-512'
ssl_cafile = './secrets/CARoot.pem'
ssl_certfile = './secrets/certificate.pem'
ssl_keyfile = './secrets/key.pem'

# Gọi hàm để liệt kê các topic
list_topics(bootstrap_servers, security_protocol, sasl_mechanism, ssl_cafile, ssl_certfile, ssl_keyfile)

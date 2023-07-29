import sys
from confluent_kafka.admin import AdminClient, NewTopic, AclBindingFilter, AclOperation, AclPermissionType, AclBinding
import subprocess
import asyncio
import random
import string

def generate_random_password():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(20))

def create_user(username, password):
    kafka_exec_command = [
        'docker',
        'exec',
        '-it',
        'kafka',
        'kafka-configs',
        '--zookeeper',
        '192.168.0.86:2181',
        '--describe',
        '--entity-type',
        'users'
    ]
    result =  subprocess.run(kafka_exec_command, capture_output=True, text=True)
    
    user_exists = False
    check_username = "user-principal '"+username+"'"
    if check_username in result.stdout:
        user_exists = True

    if user_exists:
        print(f"User {username} already exists.")
        return
    else:
        docker_exec_command = [
            'docker',
            'exec',
            '-it',
            'kafka',
            'kafka-configs',
            '--zookeeper',
            '192.168.0.86:2181',
            '--alter',
            '--add-config',
            f'SCRAM-SHA-512=[password={password}]',
            '--entity-type',
            'users',
            '--entity-name',
            username
        ]
        subprocess.run(docker_exec_command, stdout=subprocess.DEVNULL)
        print('Username:', serial_number)
        print('Password:', password)
        return

def add_permission(username, topic, group_id):
    kafka_exec_command = [
        'docker',
        'exec',
        '-it',
        'kafka',
        'kafka-acls',
        '--authorizer-properties',
        'zookeeper.connect=192.168.0.86:2181',
        '--add',
        '--allow-principal',
        username,
        '--topic',
        topic
    ]

    docker_exec_add_permission = kafka_exec_command + [
        '--operation', 
        'Create',
        '--operation',
        'Read',
        '--operation',
        'Write',
        '--operation',
        'Describe'
    ]
    docker_exec_add_group_id = kafka_exec_command + [
        '--consumer',
        '--group',
        group_id
    ]

    subprocess.run(docker_exec_add_permission, stdout=subprocess.DEVNULL)
    subprocess.run(docker_exec_add_group_id, stdout=subprocess.DEVNULL)  
    print("Successfully granted permission to topic "+topic+" for "+ username ) 
    return

async def topic_exists(admin_client, topic_name):
    topic_metadata = admin_client.list_topics().topics
    return topic_name in topic_metadata

async def create_topic(bootstrap_servers, security_protocol, sasl_mechanism, ssl_cafile, ssl_certfile, ssl_keyfile, serial_number, num_partitions, replication_factor):
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

    topic_name_1 = 'edge_' + serial_number + '_metadata'
    topic_name_2 = 'nvr_' + serial_number + '_sr'
    principal = 'User:' + serial_number

    if await topic_exists(admin_client, topic_name_1) or await topic_exists(admin_client, topic_name_2):
        print("Topics already exist")
        return

    topic1 = NewTopic(topic_name_1, num_partitions=num_partitions, replication_factor=replication_factor)
    topic2 = NewTopic(topic_name_2, num_partitions=num_partitions, replication_factor=replication_factor)

    fs = admin_client.create_topics([topic1, topic2])

    # Wait for each operation to finish.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))
    add_permission(principal, topic_name_1,"my-consumer-group")
    add_permission(principal, topic_name_2,"my-consumer-group")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 createTopic.py <serial_number>')
        sys.exit(1)

    serial_number = sys.argv[1]
    password = generate_random_password()
    bootstrap_servers = 'kafka.tungvt.vn:9094'
    security_protocol = 'SASL_SSL'
    sasl_mechanism = 'SCRAM-SHA-512'
    ssl_cafile = '/home/dep/dascam/kafka/secrets/CARoot.pem'
    ssl_certfile = '/home/dep/dascam/kafka/secrets/certificate.pem'
    ssl_keyfile = '/home/dep/dascam/kafka/secrets/key.pem'
    num_partitions = 3
    replication_factor = 1
    create_user(serial_number, password)
    asyncio.run(create_topic(bootstrap_servers, security_protocol, sasl_mechanism, ssl_cafile, ssl_certfile, ssl_keyfile, serial_number, num_partitions, replication_factor))

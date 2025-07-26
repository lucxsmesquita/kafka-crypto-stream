import os
import sys
from configparser import RawConfigParser
from json import loads

from kafka import KafkaConsumer
from pymongo import MongoClient

def get_consumer(consumer: KafkaConsumer, collection):
    for msg in consumer:
        print(f"Mensagem recebida: {msg.value}")
        print(f"Offset: {msg.offset}")
        record = msg.value
        collection.insert_one(record)


def main():
    #
    conf_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(conf_dir, "..", "crypto_config.conf")

    #
    config_local = RawConfigParser()
    config_local.read(config_path)

    #
    server = config_local["Host"]["ip"]
    port = config_local["Host"]["port"]

    #
    client = MongoClient(config_local['MongoDB']['url'])
    db = client[config_local['MongoDB']['database']]
    collection = db[config_local['MongoDB']['collection']]

    
    try:
        consumer = KafkaConsumer(
            "crypto-topic",
            bootstrap_servers=[f"{server}:{port}"],
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="crypto_topic_consumer",
            value_deserializer=lambda x: loads(x.decode("utf-8")),
        )

        print("🟢 Ouvindo o tópico Kafka...")
        print("Aguardando mensagens...")
        get_consumer(consumer, collection)
    except KeyboardInterrupt:
        print("Processo interrompido pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"Erro ao criar o consumidor: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

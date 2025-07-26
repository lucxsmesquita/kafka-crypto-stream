import os
import time
from configparser import RawConfigParser
from datetime import datetime
from json import dumps

import requests
from kafka import KafkaProducer
import sys


def fetch_crypto_api(
    crypto_coin_api: str, crypto_coin_key: str, producer: KafkaProducer
):
    url = f"{crypto_coin_api}?apiKey={crypto_coin_key}"
    response = requests.get(url)
    resultado = response.json()
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    top = {}

    top["timestamp"] = current_timestamp
    top["data"] = resultado["data"][:5]
    producer.send("crypto-topic", value=top)
    print(top)


def main():
    #
    conf_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(conf_dir, "..", "crypto_config.conf")

    config_local = RawConfigParser()
    config_local.read(config_path)

    #
    crypto_coin_api = config_local["CryptoCoinAPI"]["url"]
    crypto_coin_key = config_local["CryptoCoinAPI"]["api_key"]

    #
    server = config_local["Host"]["ip"]
    port = config_local["Host"]["port"]
    server = [f"{server}:{port}"]

    try:
        producer = KafkaProducer(
            bootstrap_servers=server,
            value_serializer=lambda x: dumps(x).encode("utf-8"),
        )
        while True:
            try:
                fetch_crypto_api(crypto_coin_api, crypto_coin_key, producer)
            except Exception as e:
                print(f"Erro ao chamar fetch_crypto_api: {e}")

            print("Aguardando 15 segundos...")
            time.sleep(40)
    except KeyboardInterrupt:
        print("Processo interrompido pelo usuário.")
        producer.flush()
        sys.exit(0)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

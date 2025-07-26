from kafka.admin import KafkaAdminClient, NewTopic


def create_topic_kafka(
    bootstrap_servers, topics, num_partitions=1, replication_factor=1
):
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

        topic_list = [
            NewTopic(
                name=topic,
                num_partitions=num_partitions,
                replication_factor=replication_factor,
            )
            for topic in topics
        ]

        admin_client.create_topics(new_topics=topic_list, validate_only=False)

        print(f"Tópico Criado com Sucesso: {', '.join(topics)}")
    except Exception as e:
        print(f"Erro ao Criar o Tópico: {e}")
    finally:
        admin_client.close()


def main():
    #
    bootstrap_servers = "localhost:9092"
    topics = ["crypto-topic"]

    create_topic_kafka(bootstrap_servers, topics)


if __name__ == "__main__":
    main()

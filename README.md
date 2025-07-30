# Projeto: Análise de Criptomoedas em Tempo Real

Este repositório contém o código de um projeto desenvolvido com foco em ingestão, armazenamento e visualização de dados de criptomoedas em tempo real. Utilizamos tecnologias modernas para integrar uma API pública de criptoativos, processar os dados e permitir consultas inteligentes com auxílio da OpenAI.

---

## 🧩 Tecnologias Utilizadas

- **MongoDB**: Armazenamento de dados históricos das criptomoedas.
- **Kafka**: Streaming e transporte dos dados da API para os consumidores.
- **Streamlit**: Interface web interativa para visualização e perguntas.
- **CoinCap API**: Fonte dos dados de criptoativos.
- **OpenAI GPT**: Respostas em linguagem natural com base nos dados coletados.

---

## 🚀 Funcionalidades

- Coleta de dados em tempo real da API CoinCap.
- Pipeline de streaming usando Kafka.
- Armazenamento dos dados em MongoDB.
- Visualização dos dados em Streamlit.
- Possibilidade de fazer perguntas (em linguagem natural) sobre os dados usando o modelo da OpenAI.

---

# ⚙️ Instruções para Execução


#### Suba os containers (MongoDB, Kafka e Zookeeper):

```bash
docker-compose up -d
```

#### Crie o tópico no Kafka:

```bash
python create-topic-kafka.py
```

#### Execute o produtor Kafka (em um terminal separado):

```bash
python create-producer-kafka.py
```

#### Execute o consumidor Kafka (em outro terminal):

```bash
python create-consumer-kafka.py
```


#### Inicie a interface Streamlit:

```bash
streamlit run streamlit.py
```

---

## ⚠️ Atenção
Configure sua chave da OpenAI (openai_key) no arquivo streamlit.py.

## 👨‍💻 Integrantes do Grupo

- Lucas Mesquita Oliveira  
- Lucas Gomes de Sousa  
- Felipe Wender Mendonça Martins

---

## Atençõo
- Configurar o openai_key no arquivo streamlit.py


## README by chat gepeto
## Valeu Thiago 🌊🤙


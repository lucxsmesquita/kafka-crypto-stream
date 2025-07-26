import os
import pandas as pd
import streamlit as st
import openai
from pymongo import MongoClient
from configparser import RawConfigParser

# === CONFIG LOCAL ===
conf_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(conf_dir,"..", "crypto_config.conf")
config_local = RawConfigParser()
config_local.read(config_path)

# === MONGO ===
client = MongoClient(config_local['MongoDB']['url'])
db = client[config_local['MongoDB']['database']]
collection = db[config_local['MongoDB']['collection']]

# === OPENAI ===
openai.api_key = ""

# === STREAMLIT ===
st.set_page_config(page_title="Cripto IA", layout="wide")
st.title("💹 Análise com IA: Criptomoedas")

# Carregar dados
docs = list(collection.find())
data_all = []
for doc in docs:
    data_all.extend(doc.get("data", []))
df = pd.json_normalize(data_all)

# Exibir dados
st.subheader("📈 Dados de Mercado")
st.dataframe(df[['name', 'symbol', 'priceUsd', 'changePercent24Hr']], use_container_width=True)

# Entrada de pergunta
st.subheader("🧠 Pergunte ao ChatGPT sobre o mercado")
user_input = st.text_input("Digite sua pergunta (ex: Vale a pena vender agora?)")

if user_input:
    # Prepara contexto (limita para não estourar tokens)
    df_context = df[['name', 'symbol', 'priceUsd', 'changePercent24Hr']].head(10).to_string(index=False)

    # Monta prompt
    prompt = f"""
Considere os dados de mercado abaixo:

{df_context}

Agora responda à seguinte pergunta do usuário com base nesses dados:

Pergunta: {user_input}
Resposta:
"""

    # Chamada ao modelo
    with st.spinner("Consultando ChatGPT..."):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        resposta = response['choices'][0]['message']['content']
        st.success("Resposta do ChatGPT:")
        st.write(resposta)

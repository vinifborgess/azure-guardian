import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

AZURE_LANGUAGE_KEY = os.getenv("AZURE_LANGUAGE_KEY")
AZURE_LANGUAGE_ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT")
if not AZURE_LANGUAGE_KEY or not AZURE_LANGUAGE_ENDPOINT:
    raise ValueError("Chave ou endpoint não encontrados no arquivo .env")
AZURE_LANGUAGE_ENDPOINT = AZURE_LANGUAGE_ENDPOINT.rstrip('/')

headers = {
    "Ocp-Apim-Subscription-Key": AZURE_LANGUAGE_KEY,
    "Content-Type": "application/json"
}

# Payload para Text Analytics
data = {
    "documents": [
        {
            "id": "1",
            "text": "John, shut the fuck up",
            "language": "en"
        }
    ]
}

# Análise de Sentimento
url_sentiment = f"{AZURE_LANGUAGE_ENDPOINT}/text/analytics/v3.1/sentiment"
try:
    response_sentiment = requests.post(url_sentiment, headers=headers, json=data)
    print("Sentiment Response:", response_sentiment.json())
except requests.RequestException as e:
    print(f"Erro na análise de sentimento: {e}")

# Análise de Entidades
url_entities = f"{AZURE_LANGUAGE_ENDPOINT}/text/analytics/v3.1/entities/recognition/general"
try:
    response_entities = requests.post(url_entities, headers=headers, json=data)
    print("Entities - Status Code:", response_entities.status_code)
    print("Entities Response:", response_entities.json())
except requests.RequestException as e:
    print(f"Erro na análise de entidades: {e}")

# Regra de moderação
if response_sentiment.status_code == 200:
    sentiment_data = response_sentiment.json()['documents'][0]
    if sentiment_data['sentiment'] == 'negative' and sentiment_data['confidenceScores']['negative'] > 0.9:
        print("Ação: Bloquear mensagem por toxicidade!")
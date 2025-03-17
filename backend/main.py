import os
import uuid
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from azure.cosmos import CosmosClient

# Configuração inicial
load_dotenv()
AZURE_LANGUAGE_KEY = os.getenv("AZURE_LANGUAGE_KEY")
AZURE_LANGUAGE_ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT")
AZURE_COSMOS_ENDPOINT = os.getenv("AZURE_COSMOS_ENDPOINT")
AZURE_COSMOS_KEY = os.getenv("AZURE_COSMOS_KEY")

if not AZURE_LANGUAGE_KEY or not AZURE_LANGUAGE_ENDPOINT:
    raise ValueError("Chave ou endpoint do Language não encontrados no .env")
if not AZURE_COSMOS_ENDPOINT or not AZURE_COSMOS_KEY:
    raise ValueError("Chave ou endpoint do Cosmos não encontrados no .env")

AZURE_LANGUAGE_ENDPOINT = AZURE_LANGUAGE_ENDPOINT.rstrip('/')
headers = {
    "Ocp-Apim-Subscription-Key": AZURE_LANGUAGE_KEY,
    "Content-Type": "application/json"
}

# Configuração do Cosmos DB
cosmos_client = CosmosClient(AZURE_COSMOS_ENDPOINT, AZURE_COSMOS_KEY)
database = cosmos_client.get_database_client("AzureGuardianDB")
container = database.get_container_client("BlockedMessages")

# Inicializa o app FastAPI
app = FastAPI()

# Modelo de entrada
class Message(BaseModel):
    text: str

# Mapeamento de leetspeak
LEETSPEAK_MAP = {
    '4': 'a', '1': 'i', '3': 'e', '0': 'o', '5': 's', '7': 't', '8': 'b', '@': 'a'
}
HATE_SPEECH_KEYWORDS = {"gay", "nigger", "fag", "bitch", "whore"}

# Função pra converter leetspeak
def translate_leetspeak(text: str) -> str:
    translated = text.lower()
    for leet, letter in LEETSPEAK_MAP.items():
        translated = translated.replace(leet, letter)
    return translated

# Função de moderação
def moderate_text(text: str):
    data = {"documents": [{"id": "1", "text": text, "language": "en"}]}
    url_sentiment = f"{AZURE_LANGUAGE_ENDPOINT}/text/analytics/v3.1/sentiment"
    url_entities = f"{AZURE_LANGUAGE_ENDPOINT}/text/analytics/v3.1/entities/recognition/general"
    
    response_sentiment = requests.post(url_sentiment, headers=headers, json=data).json()
    response_entities = requests.post(url_entities, headers=headers, json=data).json()
    
    sentiment = response_sentiment["documents"][0]["sentiment"]
    confidence = response_sentiment["documents"][0]["confidenceScores"]["negative"]
    entities = [entity["text"] for entity in response_entities["documents"][0]["entities"]]
    
    translated_text = translate_leetspeak(text)
    detected_hate = [word for word in HATE_SPEECH_KEYWORDS if word in translated_text]  # Define aqui
    
    if detected_hate:  # Usa depois
        result = {"action": "block", "reason": "hate_speech", "entities": entities + detected_hate}
        container.create_item({
            "id": str(uuid.uuid4()),
            "text": text,
            "reason": result["reason"],
            "entities": result["entities"]
        })
        return result
    elif sentiment == "negative" and confidence > 0.9:
        result = {"action": "block", "reason": "toxic", "entities": entities}
        container.create_item({
            "id": str(uuid.uuid4()),
            "text": text,
            "reason": result["reason"],
            "entities": result["entities"]
        })
        return result
    return {"action": "allow", "reason": "non-toxic", "entities": entities}

# Endpoint da API
@app.post("/moderate")
async def moderate_message(message: Message):
    try:
        result = moderate_text(message.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na moderação: {str(e)}")
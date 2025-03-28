from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
import uuid
import time
from typing import Dict, Optional
from azure.cosmos import CosmosClient
import azure.cognitiveservices.speech as speechsdk

app = FastAPI()

# Load environment variables
env_path = "C:/Users/Loovi/OneDrive/Desktop/main/side_projects/azure-guardian/backend/.env"
env_vars = {}
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            env_vars[key] = value

AZURE_LANGUAGE_KEY = env_vars["AZURE_LANGUAGE_KEY"]
AZURE_LANGUAGE_ENDPOINT = env_vars["AZURE_LANGUAGE_ENDPOINT"]
AZURE_COSMOS_ENDPOINT = env_vars["AZURE_COSMOS_ENDPOINT"]
AZURE_COSMOS_KEY = env_vars["AZURE_COSMOS_KEY"]
AZURE_SPEECH_KEY = env_vars["AZURE_SPEECH_KEY"]

headers = {
    "Ocp-Apim-Subscription-Key": AZURE_LANGUAGE_KEY,
    "Content-Type": "application/json"
}

client = CosmosClient(AZURE_COSMOS_ENDPOINT, AZURE_COSMOS_KEY)
database = client.get_database_client("AzureGuardianDB")
container = database.get_container_client("BlockedMessages")

speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region="eastus")
speech_config.set_profanity(speechsdk.ProfanityOption.Masked)  # Keep *** censorship
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# Session state
session_state: Dict[str, int] = {
    "strikes": 0,
    "toxic_score": 0
}
MAX_STRIKES = 3

# Request model
class ModerationRequest(BaseModel):
    text: Optional[str] = None
    use_voice: bool = False

# Leetspeak translator
def translate_leetspeak(text: str) -> str:
    leet_dict = {
        "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "0": "o",
        "@": "a", "$": "s", "!": "i", "|": "l"
    }
    return "".join(leet_dict.get(c, c) for c in text.lower())

# Voice transcription
def transcribe_speech() -> str:
    print("🎙️ Say something (listening)...")
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"✅ Recognized: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("❌ Nothing recognized.")
        return ""
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print(f"🚨 Canceled: {cancellation.reason}")
        print(f"🔧 Error: {cancellation.error_details}")
        return ""
    else:
        return ""

@app.post("/moderate")
def moderate_text(request: ModerationRequest):
    text = request.text
    use_voice = request.use_voice
    print(f"Received: text={text}, use_voice={use_voice}")

    if use_voice:
        text = transcribe_speech()

    if not text or text.strip() == "":
        return {
            "action": "allow",
            "reason": "no_input",
            "entities": [],
            "text": "[no speech detected]",
            "feedback": "🎤 No speech recognized. Try again."
        }

    # Auto-block censored content
    if any(c in text for c in ["*", "•", "×", "¤", "#"]):
        session_state["strikes"] += 1
        session_state["toxic_score"] += 75

        result = {
            "action": "block",
            "reason": "speech_sdk_censorship_detected",
            "entities": [],
            "text": text,
            "strikes": session_state["strikes"],
            "toxic_score": session_state["toxic_score"],
            "feedback": "⚠️ Censored language detected. Attempt blocked."
        }

        if session_state["strikes"] >= MAX_STRIKES:
            result["action"] = "ban"
            result["feedback"] = "🚫 You have been banned for repeated censored language."

        try:
            container.create_item({
                "id": str(uuid.uuid4()),
                "text": text,
                "reason": result["reason"],
                "entities": result["entities"]
            })
        except Exception as e:
            print(f"CosmosDB save error: {str(e)}")

        return result

    # Translate leetspeak
    translated_text = translate_leetspeak(text)
    print(f"Original: {text}, Translated: {translated_text}")

    # Azure NLP Sentiment & Entity Recognition
    data = {"documents": [{"id": "1", "text": translated_text, "language": "en"}]}
    url_sentiment = f"{AZURE_LANGUAGE_ENDPOINT}/text/analytics/v3.1/sentiment"
    url_entities = f"{AZURE_LANGUAGE_ENDPOINT}/text/analytics/v3.1/entities/recognition/general"

    try:
        response_sentiment = requests.post(url_sentiment, headers=headers, json=data).json()
        response_entities = requests.post(url_entities, headers=headers, json=data).json()
    except Exception as e:
        print(f"Azure API error: {str(e)}")
        return {
            "action": "allow",
            "reason": "api_error",
            "entities": [],
            "text": text
        }

    sentiment = response_sentiment["documents"][0]["sentiment"]
    confidence = response_sentiment["documents"][0]["confidenceScores"]["negative"]
    entities = [entity["text"] for entity in response_entities["documents"][0]["entities"]]

    print(f"Sentiment: {sentiment}, Negative Score: {confidence}, Entities: {entities}")

    if sentiment == "negative" and confidence >= 0.7:
        session_state["strikes"] += 1
        session_state["toxic_score"] += int(confidence * 100)

        result = {
            "action": "block",
            "reason": "toxic_or_hate_speech",
            "entities": entities,
            "text": text,
            "strikes": session_state["strikes"],
            "toxic_score": session_state["toxic_score"],
            "feedback": "⚠️ Toxic language detected. Strike issued."
        }

        if session_state["strikes"] >= MAX_STRIKES:
            result["action"] = "ban"
            result["feedback"] = "🚫 You have been banned for toxic behavior."

        try:
            container.create_item({
                "id": str(uuid.uuid4()),
                "text": text,
                "reason": result["reason"],
                "entities": result["entities"]
            })
        except Exception as e:
            print(f"CosmosDB save error: {str(e)}")

        return result

    return {
        "action": "allow",
        "reason": "non-toxic",
        "entities": entities,
        "text": text,
        "strikes": session_state["strikes"],
        "toxic_score": session_state["toxic_score"]
    }

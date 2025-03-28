import requests
import time

url = "http://127.0.0.1:8000/moderate"

# Mensagens simuladas de jogadores
game_messages = [
    {"player": "Player1", "text": "good game team"},
    {"player": "Player2", "text": "fuck you n1gg3r"},
    {"player": "Player3", "text": "nice play!"},
    {"player": "Player4", "text": "g4y losers suck"}
]

print("Simulando chat do jogo...")

for msg in game_messages:
    payload = {"text": msg["text"]}
    response = requests.post(url, json=payload)
    result = response.json()
    if result["action"] == "block":
        print(f"[{msg['player']}] [BLOCKED] '{msg['text']}' - {result['reason']} (entidades: {result['entities']})")
    else:
        print(f"[{msg['player']}] [ALLOWED] '{msg['text']}'")
    time.sleep(1)  # Pausa pra simular tempo real
import requests

url = "http://127.0.0.1:8000/moderate"
print("\nType a message or type 'voice' to use microphone (or 'exit' to quit):")

while True:
    msg = input("Player> ")
    if msg.lower() == "exit":
        break

    if msg.lower() == "voice":
        payload = {"text": None, "use_voice": True}
    else:
        payload = {"text": msg, "use_voice": False}

    print(f"Sending payload: {payload}")
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("API error:", response.text)
        continue

    result = response.json()
    status = result["action"].upper()

    if "toxic_score" in result:
        bar = "|" * (result["toxic_score"] // 10)
        print(f"Toxicity: [{bar:<10}] {result['toxic_score']}%")

    if status == "BLOCK":
        print(f"[BLOCKED] '{result['text']}' ⚠️ {result['feedback']}")
    elif status == "BAN":
        print(f"[BANNED] '{result['text']}' 💀 {result['feedback']}")
        break
    else:
        print(f"[ALLOWED] '{result['text']}' ✅")

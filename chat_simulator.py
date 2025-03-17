import requests

url = "http://127.0.0.1:8000/moderate"
print("Digite mensagens (ou 'sair' pra encerrar):")

while True:
    msg = input("Player> ")
    if msg.lower() == "sair":
        break
    payload = {"text": msg}
    response = requests.post(url, json=payload)
    result = response.json()
    if result["action"] == "block":
        print(f"[BLOCKED] Mensagem '{msg}' bloqueada por {result['reason']} (entidades: {result['entities']})")
    else:
        print(f"[ALLOWED] {msg}")
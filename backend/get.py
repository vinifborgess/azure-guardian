import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Obtém o valor da variável do .env
AZURE_LANGUAGE_ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT")

# Faz uma requisição GET para o endpoint
response = requests.get(AZURE_LANGUAGE_ENDPOINT)
print(response.status_code)
print(response.text)


from azure.cosmos import CosmosClient
import os
import uuid

env_path = "C:/Users/Loovi/OneDrive/Desktop/main/side_projects/azure-guardian/backend/.env"
env_vars = {}
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            env_vars[key] = value

AZURE_COSMOS_ENDPOINT = env_vars["AZURE_COSMOS_ENDPOINT"]
AZURE_COSMOS_KEY = env_vars["AZURE_COSMOS_KEY"]

client = CosmosClient(AZURE_COSMOS_ENDPOINT, AZURE_COSMOS_KEY)
database = client.get_database_client("AzureGuardianDB")
container = database.get_container_client("BlockedMessages")

# Testa inserção
test_item = {
    "id": str(uuid.uuid4()),
    "text": "Teste foda",
    "reason": "hate_speech",
    "entities": ["foda"]
}
try:
    container.create_item(test_item)
    print("Item salvo com sucesso:", test_item)
except Exception as e:
    print("Erro ao salvar:", str(e))

# Lista itens
try:
    items = list(container.read_all_items())
    print("Itens no container:", items)
except Exception as e:
    print("Erro ao listar:", str(e))

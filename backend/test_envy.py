from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv("AZURE_COSMOS_ENDPOINT"))
print(os.getenv("AZURE_COSMOS_KEY"))
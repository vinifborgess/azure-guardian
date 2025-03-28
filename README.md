# Azure Guardian 🛡️

![Azure Guardian Logo](https://github.com/vinifborgess/azure-guardian/blob/main/guardian_logo.png?raw=true)

Azure Guardian is an automated content moderation system for online games, designed to detect and block offensive messages in real time. Using artificial intelligence from Azure AI, the project analyzes text and voice chats to protect gaming communities from toxicity, harassment, and hate speech.

It uses Azure's NLP, Speech, and Cosmos DB services to detect and block toxic messages in real time — promoting healthier, more inclusive gaming environments.

---

## 🚀 How to Run Azure Guardian

### ✅ Prerequisites

- Python **3.13** installed  
- Git to clone the repository  
- Azure keys for:
  - **Speech**
  - **Language**
  - **Cosmos DB**
- `.env` file with your Azure credentials
- All dependencies listed in `requirements.txt`

---

### 📦 Setup Instructions

#### 1. Clone the Repository

```powershell
git clone <your-repo-url>
cd azure-guardian
```

#### 2. Activate the Virtual Environment

If you already have a virtual environment:

```powershell
.\venv\Scripts\activate
```

If you don't have one, create it:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

#### 3. Install Dependencies

With the virtual environment activated:

```powershell
pip install -r requirements.txt
```

---

### 🔐 Configure the `.env` File

Inside the `backend/` folder, create or edit a `.env` file and add your Azure keys:

```env
AZURE_LANGUAGE_KEY=<your-language-key>
AZURE_LANGUAGE_ENDPOINT=https://<your-endpoint>.cognitiveservices.azure.com/
AZURE_SPEECH_KEY=<your-speech-key>
AZURE_COSMOS_ENDPOINT=https://<your-cosmos>.documents.azure.com:443/
AZURE_COSMOS_KEY=<your-cosmos-key>
```

---

### 🧠 Run the Backend API

In the `backend/` folder, run the following command:

```powershell
cd backend
uvicorn main:app --reload
```

✅ Your API should be available at:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 🎛️ Run the Frontend (Streamlit)

In another terminal window (from the project root):

```powershell
streamlit run guardian_app.py
```

🔗 Open your browser and go to:  
[http://localhost:8501](http://localhost:8501)

---

### 🧪 Test the System

#### On Streamlit:

- In the text box, try typing a clearly offensive or inappropriate message.  
  → You should see it flagged as `[BLOCKED]`.

- Click the **"Use Voice"** button and say something offensive (for testing purposes only).  
  → The message should also be blocked automatically.

#### Optional: Terminal Mode

You can also test via the terminal:

```powershell
python chat_simulator.py
```

Then:

- Type an inappropriate message, or  
- Type `voice` and try speaking an offensive phrase to test speech moderation.

---

### 💡 Tips & Troubleshooting

- **Always start the backend API (`uvicorn`)** before running Streamlit or the simulator.
- Check the **uvicorn terminal logs** if something doesn't work as expected.
- If ports `8000` or `8501` are busy:
  - End the existing processes, or
  - Change the port configuration.

---

### 🧩 Tech Stack

- **Python 3.13**
- **FastAPI** (backend)
- **Streamlit** (frontend)
- **Azure Cognitive Services**
  - Speech
  - Language
- **Azure Cosmos DB**
- `.env` config with `python-dotenv`
- `asyncio` + `WebSockets`

---

### 🤖 Inspired by Ethical Game Devs

Azure Guardian promotes responsible AI in gaming — encouraging constructive communication while protecting users from harmful language.

---

**Feel free to fork, contribute, or open issues. Let’s build safer game communities together! 💙**

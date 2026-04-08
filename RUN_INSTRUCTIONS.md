# Running the Medical Jargon Simplification App

To run this application locally, follow the steps below. Once everything is started, you can access the interface at the link provided.

## 🔗 Main Application Link
Once the frontend is running, open your browser and go to:
[http://localhost:5001](http://localhost:5001)

---

## 🚀 Execution Steps

### 1. Prerequisites
Ensure you have the following installed:
- **Ollama**: With the `llama3` model downloaded (`ollama run llama3`).
- **Docker**: For running the MySQL database.
- **Python 3.10+**

### 2. Start the Database
Navigate to the `database` folder and start the containers:
```bash
cd database
docker compose up -d
```

### 3. Start the Backend
Navigate to the `backend` folder, install dependencies, and run the FastAPI server:
```bash
cd backend
# Create and activate venv if not done
source .venv/bin/activate
# Run the backend
uvicorn main:medicalsearch --host 0.0.0.0 --port 8000 --reload
```

### 4. Start the Frontend
Navigate to the `frontend` folder, install dependencies, and run the Flask app:
```bash
cd frontend
# Create and activate venv if not done
source .venv/bin/activate
# Run the frontend
python3 main.py
```

> [!NOTE]
> The frontend runs on port **5001** and communicates with the backend on port **8000**. Ensure both are running for the app to function correctly.

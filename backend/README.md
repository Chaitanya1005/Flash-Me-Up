# Flash Me Up Backend

This is the central API and background processing worker for the Flash Me Up Spaced-Repetition System.

## Features
* **FastAPI:** High-performance async routing with interactive Swagger documentation.
* **BackgroundTasks:** Background parsing of rich text formats (pdfs, pptx, txt) to avoid blocking HTTP requests.
* **SQLite:** Reliable local relational store for nested documents, users, flashcards, and review logs without the need to start a database server.
* **OpenAI LLM:** Generates precise flashcards automatically based on your documents.
* **Spaced Repetition (SM-2):** Advanced logging and adaptive review scheduling algorithm.

## Local Setup

### 1. Requirements
* Python 3.10+
* A Groq API Key

### 2. Environment Variables
Create a file named `.env` in the `backend/` directory:
```
PROJECT_NAME="Flash Me Up Backend"
DATABASE_URL="sqlite:///./flashmeup.db"
GROQ_API_KEY="your-groq-api-key-here"
```

### 3. Setup Python Environment
Open a terminal in the `backend` directory:
```bash
py -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
```

### 4. Running the Application
```bash
uvicorn app.main:app --reload --port 8080
```
The API is now running at: http://localhost:8080
Interactive Swagger documentation: http://localhost:8080/docs

## Sample API Requests

### 1. Create a User
```bash
curl -X 'POST' \
  'http://localhost:8080/api/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "student@example.com"
}'
```

### 2. Upload a Document
Upload a valid PDF, PPTX or TXT file using multipart form data.
```bash
curl -X 'POST' \
  'http://localhost:8080/api/documents/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'user_id=1' \
  -F 'file=@sample.pdf'
```
*Note: This triggers a background task that breaks the document into chunks and generates flashcards automatically.*

### 3. Fetch Due Flashcards
```bash
curl -X 'GET' \
  'http://localhost:8080/api/flashcards/due/1?limit=20' \
  -H 'accept: application/json'
```

### 4. Submit a Review
Score mapping: 1 (Red / Failed), 2 (Yellow / Difficult), 3 (Green / Easy).
```bash
curl -X 'POST' \
  'http://localhost:8080/api/flashcards/1/review' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "flashcard_id": 1,
  "score": 3
}'
```

### 5. Get User Statistics
```bash
curl -X 'GET' \
  'http://localhost:8080/api/stats/1' \
  -H 'accept: application/json'
```

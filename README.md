# Flash Me Up ⚡

**Flash Me Up** is an AI-powered flashcard generation and study platform wrapped in a sleek, high-contrast neon minimal UI. 

Tired of studying from hundreds of pages of PDFs or lengthy PPTXs? Upload your study materials, and let the backend automatically break them down into high-yield flashcards using incredibly fast LLM endpoints via Groq.

## 🚀 Key Features

* **Instant AI Flashcards**: Upload `.pdf`, `.pptx`, or `.txt` files, and our AI instantly extracts key concepts and generates optimized flashcards.
* **Sleek, Dynamic UI**: Built from the ground up with a custom deep obsidian (`#000000`) and neon-mint (`#01FFDB`) aesthetic offering fluid animations, focused study views, and zero clutter. 
* **Spaced Repetition Review (SRS)**: Built-in algorithms for *Hard / Good / Easy* review ratings to ensure you reinforce your memory efficiently.
* **Progress Tracking**: Automatic reporting for your total generated cards and overall study accuracy percentages.
* **Persistent History**: View all previously uploaded documents and re-access their specific flashcard decks via the collapsible sidebar at any time.

## 🛠️ Technology Stack

* **Frontend**: Designed with React 19 and bundled with Vite. Built entirely with heavily customized raw CSS.
* **Backend**: Blazing fast Python FastAPI architecture.
* **Database**: SQLAlchemy ORM with SQLite (local) / PostgreSQL (production ready) for durable document and card storage.
* **AI Processing**: Advanced parsing and inference integration via the Groq API.

---

## 💻 Local Development Setup

### 1. The Backend (FastAPI)
The backend service is located in the `/backend` directory.

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Or `.\venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

Create a `.env` file in your `/backend` directory with the following variables:
```env
DATABASE_URL=sqlite:///./flashcards.db
GROQ_API_KEY=your_groq_api_key_here
```

Run the backend server:
```bash
uvicorn app.main:app --reload --port 8080
```

### 2. The Frontend (React/Vite)
The frontend UI is located in the `/frontend` directory.

```bash
cd frontend
npm install
```

*(Note: When developing locally, ensure the API base URL in `frontend/src/api.js` points to `http://localhost:8080/api`)*

Run the local development server:
```bash
npm run dev
```

---

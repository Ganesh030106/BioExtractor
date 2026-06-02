# BioExtractor

> A lightweight, premium web application for extracting structured profile and bio data from unstructured text using client-supplied Gemini AI credentials.

## Table of contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Security Architecture](#security-architecture)
- [Requirements](#requirements)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [Production Deployment](#production-deployment)
- [Data Storage](#data-storage)
- [Development](#development)
- [License](#license)

---

## Overview

`BioExtractor` is a modern Python/Flask application that transforms free-form paragraphs, resumes, and bios into clean, structured JSON objects. It features a stunning glassmorphism front-end UI and utilizes the Google Gemini API for precise, intelligent profile parsing.

---

## Key Features

* **Intelligent Profile Parser**: Extracts fields including Name, Role, Company, Tech Stacks, Education, Contacts, Location, and Interests.
* **Client-First Security**: Enforces that only the user-provided Gemini API key is used, bypassing server-side configuration to isolate user credentials.
* **Modern Premium UI**: Sleek dark mode visual dashboard with micro-animations and smooth grid renders.
* **History Dashboard**: Keeps track of prior extractions with initials avatars and tag badges. Data can be exported as JSON or cleared.
* **Regex Fallback**: Serves as a local offline parser if AI parameters or API keys are missing.

---

## Security Architecture

To keep API keys confidential and prevent server-side access to individual secrets:
1. **Local Storage**: The Gemini API key is input in the settings drawer and stored solely in the client's web browser (`localStorage`).
2. **Dynamic Request Headers**: When extracting data, the key is passed directly in the custom request header `X-Gemini-API-Key`.
3. **Stateless Service**: The server dynamically configures the `google-generativeai` client per-request using the header key, ensuring zero persistent server-side storage of user keys.

---

## Requirements

* Python 3.10+
* Virtual Environment manager
* Active Google Gemini API Key ([Get a key from Google AI Studio](https://aistudio.google.com/apikey))

---

## Quickstart

### 1. Clone & Set Up Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Settings File

Copy `.env` variables or confirm standard configurations:
```
STORAGE_PATH=./extracted_data.json
```
*(Note: `GEMINI_API_KEY` is not required on the server, as each user inputs their individual key in the web UI).*

### 4. Run the Development Server

```bash
python app.py
```
Open your browser at `http://localhost:5000` to access the application.

---

## Usage

1. Open the application.
2. Click the **API Settings** gear icon in the top right.
3. Enter your personal Gemini API key and click **Save Settings**.
4. Paste your free-form bio text in the text container and click **Extract Data**.
5. View structured cards, raw JSON syntax highlighting, and history entries instantly.

### API Usage
To programmatically extract data, pass your key in the `X-Gemini-API-Key` header:
```bash
curl -X POST http://localhost:5000/api/extract \
  -H "Content-Type: application/json" \
  -H "X-Gemini-API-Key: YOUR_API_KEY" \
  -d '{"text": "My name is Ganesh, a Full Stack Developer from Chennai..."}'
```

---

## Production Deployment

### 1. Using WSGI (Gunicorn)
For robust production serving, run the application using `gunicorn`:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
(Adjust the worker count `-w` based on the server's CPU cores).

### 2. Deploying to Render
1. Connect your repository to [Render](https://render.com).
2. Create a new **Web Service**.
3. Set **Runtime** to `Python`.
4. Set the **Build Command** to:
   ```bash
   pip install -r requirements.txt
   ```
5. Set the **Start Command** to:
   ```bash
   gunicorn app:app
   ```

### 3. Docker Deployment
Create a `Dockerfile` in the project root:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```
Build and run the container:
```bash
docker build -t bioextractor .
docker run -p 5000:5000 bioextractor
```

---

## Data Storage

Extraction profiles are saved locally into `extracted_data.json` by default. This storage path can be customized using `STORAGE_PATH` in `.env` or changed inside `services/storage.py`.

---

## Development

* **Frontend**: Asset source is located in `static/style.css`, `static/script.js`, and `templates/index.html`.
* **API Endpoints**: Modified in `api/routes.py`.
* **Extraction Service**: Modified in `services/gemini_service.py` and `services/extractor.py`.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

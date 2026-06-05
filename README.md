# AutoDev — AI-Powered Full Project Generator

**Generate complete coding projects instantly with AI** — Chat with an LLM, generate full project structures, extract code files, auto-create `requirements.txt`, zip & download, and generate documentation — all in one Streamlit interface.

### ✨ Features

- **AI Chat Assistant** powered by **Ollama (Llama 3)**
- Generate full projects with folders and multiple files from natural language prompts
- Smart code block extraction from AI responses
- Automatic `requirements.txt` generation by scanning Python imports
- One-click project zipping and download
- Auto-generated `README.md` with project description
- Clean, responsive Streamlit UI

### 🚀 How It Works

1. Describe your project in the chat (e.g., "Build a FastAPI todo app with React frontend")
2. AI generates the complete project structure and code
3. Click **"Generate Files From AI Output"** to save files locally
4. Generate `requirements.txt`, README, and download as ZIP

### 🛠️ Tech Stack

- **Streamlit** — Web UI
- **Ollama** + **Llama 3** — Local AI model
- Python (with `re`, `zipfile`, `shutil`, etc.)

### 🎯 Perfect For

- Rapid prototyping
- Learning & teaching
- Bootstrapping new projects
- AI-assisted development workflows
- Demoing AI coding capabilities

---

**Run locally:**
```bash
pip install streamlit ollama
ollama run llama3
streamlit run app4.py

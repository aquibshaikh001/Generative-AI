# 🤖 Generative AI Toolkit (LangChain, Groq & Ollama)

A structured collection of Python CLI scripts and interactive **Streamlit** web applications built with **LangChain**, **Groq** (`openai/gpt-oss-20b`), and **Ollama**. Organized into modular directories (`chatmodels/`, `CineSage/`, and `embeddingmodels/`), this repository demonstrates multi-personality conversational agents, prompt-driven movie information extraction, Pydantic-validated structured JSON outputs, and local text embeddings.

## 📂 Project Structure

```text
Generative AI/
├── chatmodels/
│   ├── chat.py                                 # Basic LLM chat interaction script
│   ├── chatbot.py                              # CLI multi-personality chatbot
│   ├── localmodel.py                           # Local model chat integration
│   └── UI_Chat_bot.py                          # Streamlit UI for multi-personality chatbot
├── CineSage/
│   ├── core.py                                 # CLI Markdown movie information extractor
│   ├── core_UI.py                              # Streamlit UI for Markdown extractor
│   ├── core_structured_output_using_json.py    # CLI Pydantic structured JSON extractor
│   └── UI_core_structured_output_using_json.py # Streamlit UI for Pydantic JSON extractor
├── embeddingmodels/
│   └── embeddings.py                           # Local document embeddings with Ollama
├── .env                                        # Environment variables & API keys (ignored by Git)
├── .env.example                                # Template for required environment variables
├── .gitignore                                  # Git ignore rules (.venv, .env, __pycache__)
├── requirements.txt                            # Python dependencies
├── test.py                                     # Sandbox / testing script
└── README.md                                   # Project documentation
```

## ✨ Modules & Features

### 1. 💬 `chatmodels/` — Conversational & Multi-Personality Agents
Explore cloud and local LLM chat implementations, including a mood-based AI agent capable of switching between **Angry**, **Funny**, and **Sad** personas while preserving chat history.
* **`chat.py`** — Introductory chat model script.
* **`localmodel.py`** — Running conversational prompts against a local LLM.
* **`chatbot.py`** — Interactive terminal chatbot with selectable AI personalities.
* **`UI_Chat_bot.py`** — Streamlit web interface with a personality selector, adjustable creativity (`temperature`) slider, custom avatars, and chat history reset.

### 2. 🎬 `CineSage/` — Movie Information & Structured JSON Extractor
Extracts key details (Title, Release Year, Director, Genre, Cast, Music Credits, Ratings, Highlights) and generates concise summaries strictly from user-provided paragraphs without hallucination.
* **`core.py`** — CLI script using `ChatPromptTemplate` to output formatted Markdown.
* **`core_UI.py`** — Two-column Streamlit app featuring one-click sample text loading, temperature control, styled result cards, and `.md` download support.
* **`core_structured_output_using_json.py`** — CLI script enforcing strict schema validation using LangChain's `PydanticOutputParser` (`Movie` schema).
* **`UI_core_structured_output_using_json.py`** — Full-featured Streamlit dashboard displaying parsed metadata as visual UI cards, genre badges, cast pills, raw validated JSON, and `.json` export.

### 3. 🔢 `embeddingmodels/` — Local Vector Embeddings
* **`embeddings.py`** — Generates dense vector embeddings locally using **Ollama** (`nomic-embed-text`) with customizable dimensions (`dimensions=64`).

## 🛠️ Tech Stack

* **LLM Orchestration:** [LangChain](https://www.langchain.com/) (`langchain-core`, `langchain-groq`, `langchain-ollama`)
* **Cloud Inference:** [Groq](https://groq.com/) (`openai/gpt-oss-20b`)
* **Local Inference & Embeddings:** [Ollama](https://ollama.com/) (`nomic-embed-text`)
* **Web UI:** [Streamlit](https://streamlit.io/)
* **Schema Validation:** [Pydantic](https://docs.pydantic.dev/)
* **Environment Management:** `python-dotenv`

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd "Generative AI"
```

### 2. Set Up Virtual Environment & Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate        # On Windows (PowerShell): .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and add your Groq API key:
```bash
cp .env.example .env
```
Inside `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Setup Ollama (Optional — for `embeddingmodels/` & `localmodel.py`)
Ensure [Ollama](https://ollama.com/) is installed and pull the required local embedding model:
```bash
ollama pull nomic-embed-text
```

## 💻 Usage

Run all commands from the root `Generative AI` folder:

### Launch Streamlit Web Apps
```bash
# Mood AI Chatbot UI
streamlit run chatmodels/UI_Chat_bot.py

# CineSage: Markdown Info & Summary Extractor UI
streamlit run CineSage/core_UI.py

# CineSage: Structured Pydantic Movie Extractor UI
streamlit run CineSage/UI_core_structured_output_using_json.py
```

### Run CLI Scripts
```bash
# Terminal Multi-Personality Chatbot
python chatmodels/chatbot.py

# CineSage Terminal Markdown Extractor
python CineSage/core.py

# CineSage Terminal Structured JSON Extractor
python CineSage/core_structured_output_using_json.py

# Generate Local Text Embeddings
python embeddingmodels/embeddings.py
```

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

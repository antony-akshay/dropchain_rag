# Mini Contextual AI Assistant (RAG)

A document question-answering app powered by **FastAPI**, **ChromaDB**, **HuggingFace Embeddings**, and **Groq LLM** — all running in a single Docker command.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd dropchain_rag
```

### 2. Set up environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then fill in your API keys:

```env
HF_TOKEN=your_huggingface_token
GROQ_API_KEY=your_groq_api_key
```

> Get your Groq API key at [console.groq.com](https://console.groq.com) and your HuggingFace token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

### 3. Run the project

```bash
docker compose up --build
```

That's it! The first build will take a few minutes (downloading PyTorch and model weights). Subsequent runs will be instant.

| Service  | URL                        |
|----------|----------------------------|
| Frontend | http://localhost:5173      |
| Backend  | http://localhost:8000      |
| API Docs | http://localhost:8000/docs |

## Usage

1. Click **Upload Document** and select a `.txt` file
2. Ask questions about the document in the chat
3. Click **Clear Context** to wipe the vectorstore and start fresh

## Stopping the Project

```bash
docker compose down
```

## Configuration

All configuration is via the root `.env` file:

| Variable         | Default              | Description                        |
|------------------|----------------------|------------------------------------|
| `GROQ_API_KEY`   | *(required)*         | Groq API key for the LLM           |
| `HF_TOKEN`       | *(required)*         | HuggingFace token for model access |
| `EMBEDDING_MODEL`| `BAAI/bge-small-en-v1.5` | HuggingFace sentence embedding model |
| `GROQ_MODEL`     | `groq/compound-mini` | Groq model to use for answering    |
| `CHUNK_SIZE`     | `900`                | Text chunk size for splitting docs |
| `CHUNK_OVERLAP`  | `150`                | Overlap between chunks             |

## Architecture

```
Browser → nginx (port 5173) → /api/* proxied to → FastAPI (port 8000)
                                                        ↓
                                              ChromaDB (vectorstore)
                                              HuggingFace Embeddings
                                              Groq LLM
```

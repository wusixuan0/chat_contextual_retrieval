# LLM Conversation Contextual Retrieval

A tool to effectively search and retrieve from conversation histories of large language model (Claude, ChatGPT), thereby reducing effort re-explaining context when switching to new chat, or searching for a past decision/insight in conversation history.

I took some ideas from [Anthropic's blog](https://www.anthropic.com/news/contextual-retrieval)
- Anthropic: prompt llm to generate a concise explaination of a chunk of document based on the overall document
- Applying to llm conversation: Given a summary of conversation flow, index of the chunk, and the chunk, return a concise context for this chunk of chat based on the overal conversation flow progression.

- Anthropic: use reranking to filter relevant retrieved results
- Applying to llm conversation: temporal re-ranking to reconstruct decision/topic progression

## Why This Project Exists

When working on complex projects with Large Language Model(LLM), I often need to revisit past decisions and insights.
- Documenting in real time interrupts flow

- Let llm summarize the conversation has two problems:
  1. Some details are lost
  2. Some discussions only needed later in the project

### Get Started
download the chat history as txt file (for example `~/Downloads/claude-conversation-2025-01-09.txt`).
  - I use [this Chrome extension for Claude](https://chromewebstore.google.com/detail/claude-share/khnkcffkddpblpjfefjalndfpgbbjfpc)

git clone the repo, then setup environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

(Optional) Use prompt in `./prompt_summary_flow.txt` to summarize the conversation flow and save to a text file (e.g. `~/Downloads/flow.txt`)

add and embed a conversation history:
```
# Minimal (mandatory parameters only)
python main.py add \
    --chat_path ~/Downloads/claude-conversation-2025-01-09.txt \
    --url "https://claude.ai/chat/a729b08c-2fec-400d-b584-6e950dd5bc76"

# All parameters
python main.py add \                                         
    --chat_path ~/Downloads/claude-conversation-2025-01-09.txt \
    --url "https://claude.ai/chat/a729b08c-2fec-400d-b584-6e950dd5bc76" \
    --title "Improving LLM Context Retrieval" \
    --flow_path 
```

search in embeddings:
```
python main.py search "What are the key design decisions in this conversation?"
```

### workflow
1. Chunk text: `chat_history.txt` → `chunks.json`
2. (if conversation flow summary is provided) Add context: 
  `chunks.json` + `flow.txt` to llm → enriched `chunks.json`
3. Embed: enriched `chunks.json` → `vector_db.pkl`
4. Search: query against `vector_db.pkl`

### Issues
- Plain Text Format Issue:
  - The plain text format human: ... Claude: ... will hinder the quality of the conversation flow summary.

- similarity score low when searching keywords (exact match in conversation)

### Why I'm using text file instead of `conversations.json`
- messages in `conversations.json` is not in order

### project structure
```
/
├── data/
│   ├── chat_registry.json
│   ├── db/
│   │   └── vector_db.pkl
│   └── raw/
│       └── 934f25ea-6010-468e-8104-512b5d1c23e8.txt
├── src/
│   ├── __init__.py
│   ├── registry/                   # ChatRegistry
│   │   ├── __init__.py
│   │   └── registry.py
├── processor/                   # module for atomic processing
│   ├── __init__.py
│   └── processor.py            # Orchestrates the whole process
│   ├── chunk/               # Load text files + chunk
│   │   ├── __init__.py
│   │   └── load_chunk.py
│   ├── add_context/                # Add context to chunks
│   │   └── situate_context.py
│   ├── vector_store/               # Vector DB, loading existing db or create new db, embed, save db, similarity search
│   │   ├── __init__.py
│   │   └── vector_db.py
│   ├── util/
│   │   ├── llm_call.py
│   │   └── util.py
├── requirements.txt
├── .env
└── main.py
```

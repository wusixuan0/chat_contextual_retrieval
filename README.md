# LLM Conversation Contextual Retrieval

A tool to search through your Large Language Model (LLM) conversation histories with context awareness, helping you:
- Start a new chat without re-explaining context
- Search for a past decision/insight
- (Future Plan) Reconstruct the progression of ideas across multiple conversations

## Why This Project Exists

When working on complex projects with Large Language Model (LLM), I often need to revisit past decisions and insights.
- Letting llm summarize the conversation has two problems:
  1. Some details are lost.
  2. Some discussions only needed later in the project.
- Documenting in real time interrupts flow

### Idea Development
I took ideas from [Anthropic's blog on contextual retrieval](https://www.anthropic.com/news/contextual-retrieval)

**Anthropic**: prompt llm to generate a concise explaination of a chunk of document based on the overall document.

**Applying to LLM conversation**: Given a summary of conversation flow, index of the chunk, and the chunk, return a concise context for this chunk of chat based on the overal conversation flow progression.

**Anthropic**: prompt llm to filter & re-rank relevant retrieved results.

**Applying to LLM conversation**: temporal re-ranking to reconstruct decision/topic progression.

## Quick Start Guide
1. **Setup**
   ```bash
   git clone https://github.com/wusixuan0/chat_contextual_retrieval.git
   cd chat_contextual_retrieval
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Prepare Chat History**
   - Save your chat conversation as a text file (e.g., `~/Downloads/claude-conversation-2025-01-10.txt`)
   - One easy way is using [Claude Share Chrome Extension](https://chromewebstore.google.com/detail/claude-share/khnkcffkddpblpjfefjalndfpgbbjfpc)

3. **(Optional but Recommended) Create Flow Summary**
   - Use the prompt template in `./prompt_summary_flow.txt` to summarize your conversation. The summary should outline the main topics and progression of the discussion
   - Save the summary as a text file (e.g., `~/Downloads/flow.txt`)
   - **Why include summary**: The flow summary helps the system understand the context better and improves search results

   **Note on Manual Summary:**
   The current version requires manual creation of flow summaries. While automatic summarization is planned for future versions, I'm starting with manual input to gather feedback on the LLM conversation file format in step 1.
   
4. **Add Conversation**
   ```bash
   # Basic usage (without flow summary)
   python main.py add \
       --chat_path ~/Downloads/conversation.txt \
       --url "https://claude.ai/chat/your-chat-uuid"

   # With flow summary (recommended for better context awareness)
   python main.py add \
       --chat_path ~/Downloads/conversation.txt \
       --url "https://claude.ai/chat/your-chat-uuid" \
       --title "Project Planning Discussion" \
       --flow_path ~/Downloads/flow.txt
   ```
   **Notes**:
    - Current implementation uses the UUID in URL to identify the conversations text chunks

5. (Optional) Inspect content in vector database
   ```bash
   python main.py db
   ```
    Content is saved to ./data/db_content/db_{timestamp}.json by default

6. **Search**
   ```bash
   python main.py search "What were the key decisions made about the database?"
   ```

## Search Tips

### What Works
   - Frame questions in natural language
      - "What was the reasoning behind..."
      - Topic exploration ("Tell me about the discussion on...")
      - Decision tracking ("Why did we choose to...")
  - Include context terms when searching for specific topics
### Limitations
- **Keyword Searches** show low similarity scores


## Current Limitations (v1)
**During Embedding process**:
- inconvenient for user to use Chrome extension to download conversation history one by one. And one file processing at a time (no batch processing).
  - I've considered using `conversations.json` from [account setting](https://claude.ai/settings/account) for batch embedding, but I notice some messages are out of order in my `conversations.json`.
- Manual conversation flow summary creation
    - When implementing automatic summary, I notice the plain text format human: ... Claude: ... hinders the quality of the conversation flow summary.
    - I could convert the raw format into a structured format (JSON/XML) to preserve the turn-taking structure.

**During Seach**:
- Can't search within specific chat UUIDs
- Poor retrieval result for exact keyword matches

## Future Improvements (Planned)
- Get feedback on file format for LLM conversation history, then
  - Automated conversation flow summarization
  - Batch processing of multiple chats
  - Support for different chat formats
- Filter searches by chat UUID
- Improved keyword search accuracy using BM25

### project structure & embedding workflow
1. Chunk text: `chat_history.txt` → `chunks.json`
2. (if conversation flow summary is provided) Add context: 
  `chunks.json` + `flow.txt` to llm → enriched `chunks.json`
3. Embed: enriched `chunks.json` → `vector_db.pkl`
4. Search: query against `vector_db.pkl`
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
├── processor/                   # module for chat file processing
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

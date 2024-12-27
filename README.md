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
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py #TODO
```

### workflow
1. Download chat history. I use [this Chrome extension for Claude](https://chromewebstore.google.com/detail/claude-share/khnkcffkddpblpjfefjalndfpgbbjfpc)
2. Use prompt in `./prompt_summary_flow.txt` to summarize the conversation flow -> `flow.txt`
3. Chunk text: `chat_history.txt` → `chunks.json`
4. Add context: 
  `chunks.json` + `flow.txt` to llm → enriched `chunks.json`
3. Embed: enriched `chunks.json` → `vector_db.pkl`
4. Search: query against `vector_db.pkl`

### project structure
```
/
├── src/
│   ├── __init__.py
│   ├── process_chat/               # Load text + chunk
│   │   ├── __init__.py
│   │   └── process_chat_text.py
│   ├── add_context/                # Add context to chunks
│   │   └── situate_context.py
│   ├── vector_store/               # Vector DB, loading existing db or create new db, embed, save db, similarity search
│   │   ├── __init__.py
│   │   └── vector_db.py
├── data/
├── requirements.txt
├── .env
└── main.py
```

I added data directory to gitignore #TODO
```
./data/
  ├── raw/
  │     ├── processed_chats
  │     │   └── chat_history_processed.txt
  │     └── to_be_processed_chats  
  ├── processing_workspaces/    # Processing workspace
  │   └── chat_uuid_or_title/
  │       ├── chat_history.txt   # chat history in plain text
  │       ├── flow.txt           # Conversation flow/summary for context
  │       └── chunks.json        # Chunked + contextualized content
  └── db/
      ├── vector_db.pkl           # in memory vector DB of embeddings
      └── manifest.json           # "what's embedded?"
```

basic manifest file:
{
    "last_updated": "2024-12-26",
    "embedded_chats": [
        {
            "url": "https://claude.ai/chat/4e5db666-5634-40db-b07e-4c59464c7dad",
            "title": "Plan Chat Retrieval Project",
            "directory": "./data/chats/chat_plan_version",
            "chunk_count": 54,
            "embedded_timestamp": "2024-12-26"
        }
    ]
}

### Current Plan
**Current Stage:**
High Priority:

Move to single combined vector_db.pkl (enables searching across all chats)
Add basic manifest file (solves "what's embedded?" problem)
Add chat metadata to chunks.json (maintains traceability)

Medium Priority:

Standardize file structure (makes batch processing easier)
Add validation methods (prevents duplicate embedding)
Chain the processing flow (reduces errors)

Low Priority:

Batch processing capability
Enhanced manifest features
Processing status tracking

1. Priority Implementation:
   - Enhanced Context Generation:
     - Topic identification from flow summary
     - Simple importance weighting (high/medium/low)
   - Interaction pattern recognition

2. Evaluation & Testing:
   - Manual evaluation comparing:
     - Basic retrieval (current)
     - Contextualized retrieval (new)
     - Record qualitative observations
   - Manual chat selection for quality control

Chunking for V1:
- Use simpler token-based chunking
- Rely on context generation to compensate for splits
- (TBD) to capture key moments with chunks larger than 1000, overlap=200

### Tailoring solution to use case:
- chat history has strong temporal relevance.
- Include interaction patterns beyond just topic - consider adding dialog acts (question, explanation, exploration, decision, etc.)
- Add importance weighting - have the LLM rate how central this chunk is to the main conversation flow

### Future Plan
V2 Simplified Testing Approach:
   - Create a small test set of ~5 diverse conversations
   - Define specific use cases (e.g., "finding previous technical decisions", "recalling action items")
   - Enhanced Context Generation:
     - Basic temporal markers ("early/middle/late")
   - Larger chunks for key moments based on flow summary

V3 (Testing & Optimization):
- Proper evaluation framework
  - Create synthetic conversations with known retrieval targets
  - Define objective metrics (precision, recall for known items)
  - Compare different chunking strategies with real data
- Implement Q&A preservation if testing shows significant benefit
  separators=["\n\nHuman:", "\n\nAssistant:"] # Preserve turn boundaries

V4 (More Context enhancing):
- add BM25 if code in chat matters

V5 (enhance embedding):
- Dynamic chunk sizing based on content importance
- Context compression for older content
- Progressive disclosure based on relevance

VN
- Automated chat selection

### TODO
remove unuse packages from requirements.txt
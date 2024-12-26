### Get Started
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### workflow
1. Chunk text: `chat_history.txt` → `chunks.json`
2. Add context: 
  1. use prompt in `prompt_summary_flow.txt` to summarize the conversation flow
  2. `chunks.json` + `flow.txt` to llm → enriched `chunks.json`
3. Embed: enriched `chunks.json` → `vector_db.pkl`
4. Retrieve: query against `vector_db.pkl`

Structure (per chat):
./data/chats/chat_uuid_or_title/  # Processing workspace
  ├── chat_history.txt   # chat history in plain text
  ├── flow.txt           # Conversation flow/summary for context
  ├── chunks.json        # Chunked + contextualized content
└── vector_db.pkl      # Embeddings

./data/
  ├── raw/
        ├── processed_chats
  │         ├── chat_history.txt
        └── to_be_processed_chats  
  ├── processing_workspaces/
  │   └── chat_uuid_or_title/
  │       ├── chat_history.txt
  │       ├── flow.txt
  │       └── chunks.json
  └── vector_db/
      ├── vector_db.pkl
      └── manifest.json           # "what's embedded?"

basic manifest file:
{
  "last_updated": "2024-12-26", # this should be a timestamp automatically generated from running embed. for now i hard code.
  "embedded_chats": [
    {
      "url": "https://claude.ai/chat/4e5db666-5634-40db-b07e-4c59464c7dad",
      "title": "Plan Chat Retrieval Project",
      "directory": "./data/chats/chat_plan_version",
      "chunk_count": 54
    }
  ]
}

### Current Plan
**Current Focus: contextual embedding**
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
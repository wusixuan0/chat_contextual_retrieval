### Get Started
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

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
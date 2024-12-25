


def generate_context_prompt(flow_summary, chunk_content):
    return f"""
A section of a chat conversation and a summary of the conversation flow are attached. Please give a short succinct context to situate this chunk within the overall conversation for the purposes of improving search retrieval of the chunk. Focus on:
1. What is being discussed
2. Whether this contains a decision or insight
Answer only with the succinct context and nothing else.

Chat Section:
<chunk>
{chunk_content}
</chunk>

Conversation Flow:
<flow>
{flow_summary}
</flow>
"""

flow_summary_example = """
TOPIC: Understanding RAG Tutorial Implementation

- Initial discussion of vector database implementation
- Focus on how metadata stores complete text for later use
- Original vs modified implementations

BRANCH: Re-ranking Approaches

- Basic approach using Claude Haiku
- Advanced approach using Cohere
- Decision point on which approach might be better
LINK: Connected to main RAG implementation as a retrieval enhancement method

TOPIC: Adapting for Chat History Use Case

- Initial complex proposal with context preservation
- Simplified MVP approach
LINK: Built upon understanding of the original RAG implementation

AHA: Realization about Original Implementation

- Discovered that tutorial's VectorDB receives pre-chunked data
- Initial misunderstanding about where chunking occurs
- Clarified that chunking happens before VectorDB class
LINK: This insight affected how we approached the chat history adaptation

TOPIC: Technical Implementation Challenge

- Issue with VoyageAI embedding and Langchain Document objects
BRANCH: Two potential solutions
- Convert Document objects to plain text
- Investigate VoyageAI API documentation
LINK: This emerged from our attempt to implement the modified version

PARK: Future Enhancements

- Version 2 with context preservation
- More sophisticated chunking logic
- Chat context enhancement without overlap
LINK: These items emerged from simplifying our initial approach

AHA: MVP Approach Clarity

- Recognition that simpler implementation could work for initial version
- Understanding that complex features could be added later
LINK: This realization helped focus our technical implementation discussion

This conversation demonstrates how we iteratively refined our understanding and approach, moving from complex possibilities to a focused MVP implementation while noting future enhancements.
"""

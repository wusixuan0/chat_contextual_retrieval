
from src.util.llm_call import get_llm
from src.util.util import read_text_file, write_json_file, load_json_file

def situate_context(chunk_file_path, text_file_path):
    formatted_chunks = load_json_file(chunk_file_path)
    conversation_flow_summary = read_text_file(text_file_path)
    num_chunks = len(formatted_chunks)

    for i in range(num_chunks):
        chunk = formatted_chunks[i]

        if "context" in chunk: continue

        context_generation_prompt = generate_context_prompt(
            flow_summary=conversation_flow_summary,
            chunk_content=chunk["content"],
            index=chunk["i"],
            num_chunks=num_chunks,
        )
        try:
            print(i)
            response_text = get_llm(content=context_generation_prompt)
            chunk["context"] = response_text
        except Exception as e:
            print(f"Error occurred at chunk {i}: {str(e)}")
            write_json_file(formatted_chunks, chunk_file_path)
            raise
    write_json_file(formatted_chunks, chunk_file_path)

def generate_context_prompt(flow_summary, chunk_content, index, num_chunks):
    return f"""
A chunk of a chat conversation and a summary of the conversation flow are provided below.

Your task is to provide a succinct context for this chat chunk by drawing upon the provided Conversation Flow, ensuring this context effectively connects the chunk to the broader themes, topics, and developments outlined in the flow with the goal of improving its discoverability through future search.

**Task Instructions:**
- **Connecting to the Broader Flow:** Chunk's Location is {index+1} of {num_chunks} total chunks. Use the conversation flow summary and chunk's location to situate the chunk within the conversation and understand the broader context surrounding this specific chunk. Determine this chunk's role and relevance by identifying its connections to the Conversation Flow.
- **Brevity for Less Important Chunks:** For chunks that represent minor clarifications, quick agreements, or other less significant points, a single-sentence context is sufficient.

**Example of an Effective Context:**
For a chat chunk containing "Key architectural decisions made regarding [mention specific aspect].", an effective context would be: "Key architectural decisions made regarding [mention specific aspect]. This aligns with the 'Initial complex proposal' outlined previously and represents a significant shift in the system design."

**Example of an Effective Context (Less Important Chunk):**
For a chat chunk containing "When we say 'API endpoint,' are we referring to the v2 or the legacy one? Let's stick with v2 for now...", an effective context would be: "Clarification on the specific API endpoint version being used (v2)."

** Chat Chunk: **
<chunk>
{chunk_content}
</chunk>

** Conversation Flow Summary: **
<flow>
{flow_summary}
</flow>

Answer only with the succinct context and nothing else.
"""

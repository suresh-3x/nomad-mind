import subprocess
from vectorstore import search_similar

def query_llm(question):
    docs = search_similar(question)
    context = "\n".join(docs)
    
    print(context)
    prompt = f"""You are a travel planner AI. Based on the following vlog transcript excerpts, answer the question.\n
Context:
{context}

Question: {question}
Answer:"""

    result = subprocess.run(
        ["ollama", "run", "llama3.1"],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()


def generate_itinerary(selected_vid_ids):
    all_chunks = []
    for vid in selected_vid_ids:
        results = collection.get(where={"id": {"$contains": vid}})
        all_chunks.extend(results["documents"])
    context = "\n".join(all_chunks)

    prompt = f"""You are a travel agent AI. Based on the transcript snippets below, create a 3-day travel itinerary including:
- Morning, afternoon, and evening suggestions
- Food spots
- Activities
- Local tips

Transcript snippets:
{context}

--- Itinerary Start ---
"""
    result = subprocess.run(["ollama", "run", "llama3"], input=prompt.encode(), stdout=subprocess.PIPE)
    return result.stdout.decode()





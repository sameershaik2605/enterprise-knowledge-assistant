# llm.py
# A single reusable function for talking to your local LLM.
# Every later part of the project (retrieval, summarization, comparison,
# keyword extraction) will import and call this same function.

import ollama

MODEL_NAME = "llama3.1:8b"  # change to "phi3" here if you're using the lighter model

def ask_llm(prompt: str) -> str:
    """Send a prompt to the local LLM and return its text response."""
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


if __name__ == "__main__":
    # Quick manual test — run this file directly to confirm it works:
    # python llm.py
    answer = ask_llm("Say hello in one sentence.")
    print(answer)
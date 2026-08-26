"""Using Ollama local LLM AI model to analyze the data."""

import time
from pathlib import Path

# pip install ollama
from ollama import chat  # type: ignore

MODEL = "qwen3:latest"
# deepseek-r1:latest
# llama3.2:latest
# qwen3:latest
# mistral:latest

MSG_CONTEXT = Path("src/ai_ollama_prompt.md").read_text()

cont = Path("data/join.json").read_text()

time_start = time.time()
stream = chat(
    model=MODEL,
    messages=[
        {
            "role": "system",
            # "role": "user",
            # 5 data sources: Sleep data, sport activities, calendar entries,
            #  coding commits, personal journal.
            "content": MSG_CONTEXT,
        },
        {"role": "user", "content": cont},
    ],
    stream=True,
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
print()

print(f"{round(time.time() - time_start)}s")

import requests

def ask_llm(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 1024,
                    "num_ctx": 2048
                }
            },
            timeout=300
        )
        return response.json()["response"]

    except Exception as e:
        return f"[LLM ERROR] {str(e)}"
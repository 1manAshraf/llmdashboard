import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "llama3.2:latest"


def ask_llm(prompt):
    """
    Send a prompt to the local Ollama instance.

    Returns:
        str: LLM response or a readable error message.
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 1024,
                    "num_ctx": 4096
                }
            },
            timeout=600
        )

        response.raise_for_status()

        data = response.json()

        if "response" not in data:
            return "[LLM ERROR] Ollama returned no response."

        return data["response"].strip()

    except requests.exceptions.ConnectionError:
        return (
            "[LLM ERROR] Cannot connect to Ollama. "
            "Make sure Ollama is running on localhost:11434."
        )

    except requests.exceptions.Timeout:
        return (
            "[LLM ERROR] Ollama request timed out "
            "after 10 minutes."
        )

    except requests.exceptions.RequestException as e:
        return f"[LLM ERROR] Ollama request failed: {e}"

    except Exception as e:
        return f"[LLM ERROR] Unexpected error: {e}"

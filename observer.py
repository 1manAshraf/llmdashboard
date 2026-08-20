from llm_client import ask_llm

def observe(raw_output):
    print("\n[OBSERVER] Analysing output...")

    # Trim output if too long
    if len(raw_output) > 2000:
        raw_output = raw_output[:2000]

    prompt = f"""Analyse this penetration test output in 5 lines max.
List only: open ports, service versions, and top vulnerability to exploit next.

Output:
{raw_output}"""

    result = ask_llm(prompt)
    print("[OBSERVER] Done.")
    return result
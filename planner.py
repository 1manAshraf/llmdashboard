from llm_client import ask_llm

def plan_next_action(target_ip, findings, history):
    print("\n[PLANNER] Planning next action...")

    # Only keep last 4 history items to keep prompt short
    recent_history = history[-4:] if len(history) > 4 else history
    history_text = "\n".join(recent_history)

    prompt = f"""You are a penetration tester. Target: {target_ip}

Recent actions:
{history_text}

Latest findings:
{findings}

Reply with ONE shell command to run next. No explanation. No extra words.
If testing is complete, reply: DONE"""

    result = ask_llm(prompt)

    for line in result.strip().split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            print(f"[PLANNER] Next: {line}")
            return line

    return "DONE"
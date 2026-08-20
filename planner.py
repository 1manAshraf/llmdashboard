from llm_client import ask_llm


def plan_next_action(target_ip, findings, history, log_callback=None):

    def log(message):
        print(message)

        if log_callback:
            log_callback(message)

    log("[PLANNER] Planning next reconnaissance action...")

    recent_history = history[-4:] if len(history) > 4 else history

    history_text = "\n".join(recent_history)

    prompt = f"""
You are an authorized penetration-testing assistant operating
inside an isolated security laboratory.

Target:
{target_ip}

Recent activity:
{history_text}

Latest findings:
{findings}

Choose ONE additional Nmap reconnaissance command.

Allowed command format examples:

nmap -sV -p PORT {target_ip}

or:

nmap -sV -p PORT1,PORT2 {target_ip}

Do not provide:
- exploitation commands
- shell commands
- file operations
- download commands
- privilege escalation commands
- commands against another IP

If no additional reconnaissance is necessary, reply exactly:

DONE

Return ONLY the Nmap command or DONE.
"""

    result = ask_llm(prompt).strip()

    if result.startswith("[LLM ERROR]"):
        log(result)
        return "DONE"

    if result.upper() == "DONE":
        log("[PLANNER] Testing complete.")
        return "DONE"

    # Find the first line that looks like an Nmap command.
    for line in result.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.lower().startswith("nmap "):

            # Make sure the target appears in the command.
            if target_ip in line:

                log(f"[PLANNER] Next action: {line}")

                return line

    log("[PLANNER] No valid Nmap command returned.")
    return "DONE"

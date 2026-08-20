from llm_client import ask_llm


def observe(raw_output, log_callback=None):

    def log(message):
        print(message)

        if log_callback:
            log_callback(message)

    log("[OBSERVER] Analysing Nmap output...")

    if not raw_output:
        return "[OBSERVER ERROR] No output received."

    if len(raw_output) > 2000:
        raw_output = raw_output[:2000]

    prompt = f"""
You are analysing an authorized penetration-testing lab scan.

Analyse the following Nmap output.

Return no more than 5 lines.

List only:
- open ports
- detected service versions
- potential vulnerability
- recommended Nmap reconnaissance step

Do not provide arbitrary shell commands.

Nmap output:

{raw_output}
"""

    result = ask_llm(prompt)

    if result.startswith("[LLM ERROR]"):
        log(result)
        return result

    log("[OBSERVER] Analysis completed.")

    return result

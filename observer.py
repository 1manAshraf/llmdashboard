from llm_client import ask_llm


def observe(raw_output, log_callback=None):

    def log(message):
        print(message)

        if log_callback:
            log_callback(message)

    log("[OBSERVER] Analysing Nmap output...")

    # ========================================================
    # CHECK OUTPUT
    # ========================================================

    if not raw_output:
        return "[OBSERVER ERROR] No output received."

    # Limit the amount of data sent to the LLM.
    if len(raw_output) > 4000:
        raw_output = raw_output[:4000]

    # ========================================================
    # STRUCTURED ANALYSIS PROMPT
    # ========================================================

    prompt = f"""
You are the observation component of an authorized
penetration-testing laboratory system.

Your job is ONLY to extract information explicitly present
in the Nmap output.

Do NOT guess.

Do NOT invent:
- vulnerabilities
- CVEs
- software versions
- operating systems
- credentials
- exploitation results
- attack success
- security ratings

If information is not explicitly present, write:
NOT STATED

For every detected service, return exactly this format:

PORT: <port number>
PROTOCOL: <protocol>
SERVICE: <service name or NOT STATED>
VERSION: <exact version from Nmap or NOT STATED>
EVIDENCE: <short quotation/paraphrase of what Nmap reported>
STATUS: CANDIDATE

If a possible security concern is directly supported by the
Nmap output, add:

POTENTIAL ISSUE: <issue>
BASIS: <exact evidence supporting the issue>

Otherwise write:

POTENTIAL ISSUE: NONE
BASIS: NONE

Important:

A service being open does NOT automatically mean it is
vulnerable.

Do not classify a vulnerability as VERIFIED.

Return only information supported by the Nmap output.

NMAP OUTPUT:

{raw_output}
"""

    # ========================================================
    # ASK LLM
    # ========================================================

    result = ask_llm(prompt)

    # ========================================================
    # LLM ERROR
    # ========================================================

    if result.startswith("[LLM ERROR]"):

        log(result)

        return result

    # ========================================================
    # SUCCESS
    # ========================================================

    log("[OBSERVER] Structured analysis completed.")

    return result

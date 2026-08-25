from llm_client import ask_llm
from parser import (
    parse_nmap_output,
    format_evidence_for_llm
)


def observe(raw_output, log_callback=None):

    def log(message):
        print(message)

        if log_callback:
            log_callback(message)

    log("[OBSERVER] Parsing Nmap evidence...")

    if not raw_output:
        return "[OBSERVER ERROR] No output received."

    # ========================================================
    # PARSE NMAP OUTPUT
    # ========================================================

    evidence = parse_nmap_output(raw_output)

    if not evidence["ports"]:
        log("[OBSERVER] No ports detected.")
        return "[OBSERVER] No verified open ports detected."

    # ========================================================
    # FORMAT VERIFIED EVIDENCE
    # ========================================================

    structured_evidence = format_evidence_for_llm(evidence)

    log(
        f"[OBSERVER] Parsed {len(evidence['ports'])} port entries."
    )

    # ========================================================
    # LLM ANALYSIS
    # ========================================================

    prompt = f"""
You are an authorized penetration-testing assistant
operating inside an isolated security assessment laboratory.

You are given VERIFIED evidence extracted from Nmap.

Your job is to analyse the evidence.

IMPORTANT RULES:

1. Only use information explicitly present in the evidence.
2. Do NOT invent vulnerabilities.
3. Do NOT invent CVEs.
4. Do NOT assume that an old software version automatically
   means a specific vulnerability exists.
5. Do NOT claim exploitation occurred.
6. Do NOT claim credentials were discovered.
7. Do NOT invent operating-system details.
8. Do NOT provide arbitrary shell commands.
9. If evidence is insufficient to identify a vulnerability,
   explicitly say so.
10. Distinguish between:
    - observed fact
    - potential security concern
    - information that requires further verification.

Return no more than 8 lines.

Use this format:

OPEN PORTS:
SERVICE VERSIONS:
SECURITY CONCERNS:
EVIDENCE LIMITATIONS:
RECOMMENDED RECONNAISSANCE:

VERIFIED NMAP EVIDENCE:

{structured_evidence}
"""

    result = ask_llm(prompt)

    # ========================================================
    # LLM ERROR
    # ========================================================

    if result.startswith("[LLM ERROR]"):

        log(result)

        # Return the verified evidence even if
        # the LLM is unavailable.

        return structured_evidence

    log("[OBSERVER] Evidence analysis completed.")

    return (
        "VERIFIED EVIDENCE:\n"
        + structured_evidence
        + "\n\n"
        "LLM ANALYSIS:\n"
        + result
    )

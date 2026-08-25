from llm_client import ask_llm
from parser import format_evidence_for_llm
from datetime import datetime
from pathlib import Path


REPORT_DIRECTORY = Path("reports")


def generate_report(
    target_ip,
    parsed_evidence,
    time_taken="N/A"
):

    print("\n[ANALYSER] Generating report...")

    REPORT_DIRECTORY.mkdir(exist_ok=True)

    # ========================================================
    # VERIFIED EVIDENCE
    # ========================================================

    verified_evidence = format_evidence_for_llm(
        parsed_evidence
    )

    print("\n[ANALYSER] Verified evidence sent to LLM:")
    print(verified_evidence)

    # ========================================================
    # LLM PROMPT
    # ========================================================

    prompt = f"""
You are a cybersecurity report writer working in an
authorized penetration-testing laboratory.

Your job is to write a professional security assessment
report using ONLY the VERIFIED NMAP EVIDENCE below.

IMPORTANT EVIDENCE RULES:

The verified evidence is the source of truth.

DO NOT invent:

- ports
- services
- service versions
- vulnerabilities
- CVEs
- exploits
- credentials
- attack success
- operating systems
- technologies
- configurations
- security controls

DO NOT change a port number.

For example:

If the evidence says:

512/tcp

you MUST NOT report:

513/tcp

If a vulnerability is not directly supported by the
evidence, do not claim that the vulnerability exists.

An outdated software version alone does NOT prove that
a specific vulnerability exists.

Do not invent CVEs from memory.

Do not claim that a service is exploitable.

Do not claim that penetration was successful.

Clearly distinguish between:

1. Verified findings
2. Security observations
3. Recommendations

For example:

Telnet being detected may be described as a security
concern because Telnet communicates without encryption.

However, do not claim that the target was successfully
compromised.

Do not generate attack commands.

Do not generate Metasploit commands.

Do not generate shell commands.

Do not recommend attacking another host.

--------------------------------------------------
VERIFIED NMAP EVIDENCE
--------------------------------------------------

{verified_evidence}

--------------------------------------------------

Target:
{target_ip}

Date:
{datetime.now().strftime("%Y-%m-%d")}

Time taken:
{time_taken}

--------------------------------------------------

Generate a professional penetration-testing report.

Use exactly these sections:

1. Executive Summary

2. Reconnaissance Findings

3. Services Detected

4. Security Observations

5. Risk Rating

6. Recommendations

--------------------------------------------------

REQUIREMENTS FOR EACH SECTION

Executive Summary:
Summarize what was actually detected.

Reconnaissance Findings:
List only verified Nmap findings.

Services Detected:
List the detected ports, services and versions.

Security Observations:
Only identify security concerns supported by
the verified evidence.

If there is insufficient evidence for a vulnerability,
explicitly state:

"No confirmed vulnerability identified from the
available Nmap evidence."

Risk Rating:
Use one of:

Informational
Low
Medium
High

Do not assign a high rating without sufficient evidence.

Recommendations:
Provide defensive recommendations based on the
detected services.

Do not invent vulnerabilities to justify recommendations.

--------------------------------------------------

IMPORTANT:

The final report must never contain facts that are
different from the VERIFIED NMAP EVIDENCE.
"""

    # ========================================================
    # ASK LLM
    # ========================================================

    report = ask_llm(prompt)

    # ========================================================
    # LLM ERROR HANDLING
    # ========================================================

    if report.startswith("[LLM ERROR]"):

        report = (
            "Report generation failed because the LLM could "
            "not be reached.\n\n"
            + report
        )

    # ========================================================
    # FINAL REPORT
    # ========================================================

    final_report = (
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"Target: {target_ip}\n"
        f"Time Taken: {time_taken}\n"
        + "=" * 60
        + "\n\n"
        + report
    )

    # ========================================================
    # SAVE REPORT
    # ========================================================

    safe_target = (
        target_ip
        .replace(".", "_")
        .replace("/", "_")
    )

    filename = (
        REPORT_DIRECTORY
        / f"report_{safe_target}.txt"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(final_report)

    print(
        f"[ANALYSER] Saved: {filename}"
    )

    return final_report, str(filename)

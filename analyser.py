from llm_client import ask_llm
from datetime import datetime
from pathlib import Path


REPORT_DIRECTORY = Path("reports")


def generate_report(target_ip, history, time_taken="N/A"):

    print("\n[ANALYSER] Generating evidence-based report...")

    REPORT_DIRECTORY.mkdir(exist_ok=True)

    # ========================================================
    # PREPARE SESSION DATA
    # ========================================================

    recent = history[-6:]

    history_text = "\n\n".join(recent)

    # Prevent an excessively large prompt.
    if len(history_text) > 5000:
        history_text = history_text[:2500]

    # ========================================================
    # REPORT PROMPT
    # ========================================================

    prompt = f"""
You are the reporting component of an authorized penetration-
testing laboratory system.

Your job is to create an evidence-based security assessment
report from the supplied session information.

IMPORTANT RULES:

1. Use ONLY information explicitly contained in the session.
2. Never invent information.
3. Never assume that an old software version is vulnerable.
4. Never claim a CVE unless the session explicitly contains
   evidence for that CVE.
5. Never claim exploitation.
6. Never claim successful compromise.
7. Never claim credentials were obtained.
8. Never claim a vulnerability was verified unless the session
   explicitly contains verification evidence.
9. An open port is NOT automatically a vulnerability.
10. A detected software version is NOT automatically a
    vulnerability.
11. Do not invent operating systems or service versions.
12. Do not invent additional services.
13. Do not invent scan results.
14. Do not use information from your general knowledge to
    create vulnerabilities that are not demonstrated by the
    session.

Use these categories:

OBSERVED
---------
Information directly reported by the security tools.

CANDIDATE
---------
A potential security concern that may require additional
verification.

VERIFIED
--------
A vulnerability for which the session contains explicit
verification evidence.

If there is no verification evidence, write:

"No vulnerabilities were verified during this session."

Do NOT convert CANDIDATE findings into VERIFIED findings.

------------------------------------------------------------
TARGET
------------------------------------------------------------

{target_ip}

------------------------------------------------------------
DATE
------------------------------------------------------------

{datetime.now().strftime("%Y-%m-%d")}

------------------------------------------------------------
TIME TAKEN
------------------------------------------------------------

{time_taken}

------------------------------------------------------------
SESSION EVIDENCE
------------------------------------------------------------

{history_text}

============================================================
REPORT FORMAT
============================================================

# Penetration Testing Report

## 1. Executive Summary

Briefly summarize what was actually observed.

Clearly state whether vulnerabilities were verified.

Do not exaggerate the results.

## 2. Reconnaissance Findings

List only information directly supported by the session.

Include:

- Target
- Open ports
- Protocols
- Services
- Versions
- Other directly observed information

## 3. Observed Services

Create a simple list or table containing:

Port | Protocol | Service | Version | Evidence

Only include services actually present in the session.

## 4. Candidate Security Issues

List potential security concerns that are supported by
the evidence.

For each candidate include:

Issue:
Evidence:
Why further verification may be appropriate:
Status: CANDIDATE

Do not call these vulnerabilities.

If there are none, write:

"No candidate security issues were identified."

## 5. Verified Vulnerabilities

Only include vulnerabilities that have explicit verification
evidence in the session.

For each verified vulnerability include:

Vulnerability:
Evidence:
Verification:
Status: VERIFIED

If none were verified, write:

"No vulnerabilities were verified during this session."

## 6. Risk Assessment

Do NOT assign a risk rating to an unverified vulnerability.

If no vulnerabilities were verified, state:

"Overall risk could not be determined from verified
vulnerability evidence. Further verification is recommended."

You may describe the attack surface based on observed services,
but do not turn that observation into a vulnerability rating.

## 7. Recommendations

Recommendations must correspond to observed services or
candidate findings.

Do not recommend fixing vulnerabilities that were never
identified.

============================================================

Return ONLY the report.

SESSION EVIDENCE:

{history_text}
"""

    # ========================================================
    # CALL LLM
    # ========================================================

    report = ask_llm(prompt)

    # ========================================================
    # HANDLE LLM ERROR
    # ========================================================

    if report.startswith("[LLM ERROR]"):

        report = (
            "Report generation failed because the LLM could not "
            "be reached.\n\n"
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
    # FILE NAME
    # ========================================================

    safe_target = (
        target_ip
        .replace(".", "_")
        .replace("/", "_")
    )

    filename = (
        REPORT_DIRECTORY /
        f"report_{safe_target}.txt"
    )

    # ========================================================
    # SAVE REPORT
    # ========================================================

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(final_report)

    print(
        f"[ANALYSER] Evidence-based report saved: {filename}"
    )

    return final_report, str(filename)

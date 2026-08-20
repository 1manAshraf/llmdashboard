from llm_client import ask_llm
from datetime import datetime
from pathlib import Path


REPORT_DIRECTORY = Path("reports")


def generate_report(target_ip, history, time_taken="N/A"):

    print("\n[ANALYSER] Generating report...")

    REPORT_DIRECTORY.mkdir(exist_ok=True)

    recent = history[-6:]

    history_text = "\n\n".join(recent)[:4000]

    prompt = f"""
Write a penetration-testing report for an authorized security
assessment lab.

Target:
{target_ip}

Date:
{datetime.now().strftime("%Y-%m-%d")}

Time taken:
{time_taken}

Session:
{history_text}

Only report vulnerabilities that are actually supported by
the scan/session information.

Sections:

1. Executive Summary
2. Reconnaissance Findings
3. Services Detected
4. Potential Vulnerabilities
5. Risk Rating
6. Recommendations

Do not invent vulnerabilities, CVEs, credentials, exploitation
results, or attack success that are not supported by the session.
"""

    report = ask_llm(prompt)

    if report.startswith("[LLM ERROR]"):
        report = (
            "Report generation failed because the LLM could not "
            "be reached.\n\n"
            + report
        )

    final_report = (
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"Target: {target_ip}\n"
        f"Time Taken: {time_taken}\n"
        + "=" * 60
        + "\n\n"
        + report
    )

    safe_target = target_ip.replace(".", "_").replace("/", "_")

    filename = REPORT_DIRECTORY / f"report_{safe_target}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_report)

    print(f"[ANALYSER] Saved: {filename}")

    return final_report, str(filename)

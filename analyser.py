from llm_client import ask_llm
from datetime import datetime
from pathlib import Path


REPORT_DIRECTORY = Path("reports")


def build_verified_evidence(parsed_evidence):
    """
    Convert parser output into a strict evidence block.

    The LLM must only use information contained here.
    """

    lines = []

    lines.append("VERIFIED NMAP EVIDENCE")
    lines.append("=" * 40)

    lines.append(
        f"Target: {parsed_evidence.get('target', 'Unknown')}"
    )

    lines.append(
        f"Host Up: {parsed_evidence.get('host_up', 'Unknown')}"
    )

    lines.append("")
    lines.append("Detected Ports:")

    ports = parsed_evidence.get("ports", [])

    if ports:

        for port in ports:

            lines.append(
                f"- {port.get('port')}/"
                f"{port.get('protocol', 'tcp')} | "
                f"{port.get('state')} | "
                f"{port.get('service')} | "
                f"{port.get('version', 'Unknown')}"
            )

    else:

        lines.append("- No verified open ports.")

    os_info = parsed_evidence.get("os", [])

    if os_info:

        lines.append("")
        lines.append("OS Information:")

        for os_name in os_info:
            lines.append(f"- {os_name}")

    return "\n".join(lines)


def generate_report(
    target_ip,
    parsed_evidence,
    time_taken="N/A"
):

    print("\n[ANALYSER] Generating report...")

    REPORT_DIRECTORY.mkdir(exist_ok=True)

    verified_evidence = build_verified_evidence(
        parsed_evidence
    )

    prompt = f"""
You are a cybersecurity report writer.

You are writing a report for an authorized penetration-testing
laboratory.

IMPORTANT RULE:

The VERIFIED NMAP EVIDENCE below is the ONLY source of truth.

You MUST NOT invent:

- CVEs
- vulnerabilities
- exploits
- credentials
- attack success
- software versions
- operating systems
- security weaknesses
- technologies
- services
- vulnerability names

If a vulnerability cannot be directly supported by the
verified evidence, do NOT report it as a vulnerability.

You may identify an obvious security concern when it is directly
supported by the evidence.

For example:

If Telnet is explicitly detected:
You may state that Telnet is an insecure, unencrypted protocol.

If an old software version is explicitly detected:
You may state that the software version is outdated or should
be reviewed.

However, do NOT assign a specific CVE unless the evidence
explicitly contains that CVE.

Do not infer vulnerabilities merely from a software version.

Do not claim that a service is exploitable.

Do not claim that exploitation was successful.

Do not mention tools that are not present in the evidence.

Use only the verified information below.

--------------------------------------------------
VERIFIED EVIDENCE
--------------------------------------------------

{verified_evidence}

--------------------------------------------------

Target:
{target_ip}

Date:
{datetime.now().strftime("%Y-%m-%d")}

Time taken:
{time_taken}

Generate the report using exactly these sections:

1. Executive Summary
2. Reconnaissance Findings
3. Services Detected
4. Security Observations
5. Risk Rating
6. Recommendations

For Security Observations:

Only include observations supported by the evidence.

For Risk Rating:

Use:
- Informational
- Low
- Medium
- High

Do not assign a high or critical rating without sufficient
evidence.

For Recommendations:

Give defensive recommendations based only on the detected
services and information.

Do not recommend exploitation.

Do not generate Nmap commands.

Do not generate Metasploit commands.

Do not generate shell commands.

The report must clearly distinguish between:

- verified facts
- security observations
- recommendations

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

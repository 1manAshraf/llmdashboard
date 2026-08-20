from llm_client import ask_llm
from datetime import datetime

def generate_report(target_ip, history, time_taken="N/A"):
    print("\n[ANALYSER] Generating report...")

    recent = history[-6:]
    history_text = "\n\n".join(recent)[:2000]

    prompt = f"""Write a penetration test report. Target: {target_ip}. Date: {datetime.now().strftime("%Y-%m-%d")}.
Time taken: {time_taken}.

Session:
{history_text}

Known CVE reference list for Metasploitable 2 services (use the matching CVE if the service below was found in the session):
- vsftpd 2.3.4 -> CVE-2011-2523 (backdoor command execution)
- OpenSSH 4.7p1 -> CVE-2008-0166 (weak key generation, Debian OpenSSL)
- Apache 2.2.8 -> CVE-2009-1195 (mod_perl arbitrary code execution)
- Samba 3.X smbd -> CVE-2007-2447 (usermap_script remote code execution)
- UnrealIRCd -> CVE-2010-2075 (backdoor command execution)
- ProFTPD 1.3.1 -> CVE-2010-4221 (telnet IAC stack overflow)
- MySQL 5.0.51a -> CVE-2009-2446 (authentication bypass)
- PostgreSQL 8.3 -> CVE-2013-1899 (authentication bypass)
- Apache Tomcat (manager) -> CVE-2009-3548 (arbitrary file upload)
- distccd -> CVE-2004-2687 (remote command execution)
- ISC BIND 9.4.2 -> CVE-2008-2476 (denial of service)
- VNC (no/weak auth) -> CVE-1999-0506 (weak authentication)
- rlogin/rsh services -> CVE-1999-0651 (insecure remote shell)

Sections:
1. Executive Summary (2 sentences)
2. Vulnerabilities Found (name + CVE number from list above if it matches + severity)
3. Attack Chain (numbered steps)
4. Risk Rating (one word + one sentence)
5. Recommendations (one line each)

IMPORTANT: Only cite a CVE if the matching service/version was actually mentioned in the session above. Do not invent CVE numbers that are not in the reference list."""

    report = ask_llm(prompt)    

    final_report = f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    final_report += f"Target: {target_ip}\n"
    final_report += f"Time Taken: {time_taken}\n"
    final_report += "=" * 40 + "\n\n"
    final_report += report

    filename = f"report_{target_ip.replace('.','_')}.txt"
    with open(filename, "w") as f:
        f.write(final_report)

    print(f"[ANALYSER] Saved: {filename}")
    return final_report, filename
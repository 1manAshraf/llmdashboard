import re


def parse_nmap_output(raw_output):
    """
    Parse Nmap output into structured security evidence.

    This parser is deterministic:
    it does NOT use the LLM to decide what ports,
    services, or versions were detected.
    """

    evidence = {
        "target": None,
        "host_up": False,
        "ports": [],
        "os": [],
        "raw_output": raw_output or ""
    }

    if not raw_output:
        return evidence

    lines = raw_output.splitlines()

    # ========================================================
    # TARGET
    # ========================================================

    for line in lines:

        match = re.search(
            r"Nmap scan report for (?:[^\s]+ \()?(\d{1,3}(?:\.\d{1,3}){3})\)?",
            line
        )

        if match:
            evidence["target"] = match.group(1)
            break

    # ========================================================
    # HOST STATUS
    # ========================================================

    for line in lines:

        if "Host is up" in line:
            evidence["host_up"] = True
            break

    # ========================================================
    # PORT / SERVICE INFORMATION
    # ========================================================

    # Example:
    #
    # 21/tcp  open  ftp       vsftpd 2.3.4
    #
    # 80/tcp  open  http      Apache httpd 2.2.8 ((Ubuntu) DAV/2)
    #
    # 139/tcp open netbios-ssn Samba smbd 3.X - 4.X

    port_pattern = re.compile(
        r"^(\d+)/(tcp|udp)\s+"
        r"(open|closed|filtered)\s+"
        r"(\S+)"
        r"(?:\s+(.*))?$",
        re.IGNORECASE
    )

    for line in lines:

        line = line.strip()

        match = port_pattern.match(line)

        if not match:
            continue

        port = int(match.group(1))
        protocol = match.group(2).lower()
        state = match.group(3).lower()
        service = match.group(4)
        version = (match.group(5) or "").strip()

        port_data = {
            "port": port,
            "protocol": protocol,
            "state": state,
            "service": service,
            "version": version
        }

        evidence["ports"].append(port_data)

    # ========================================================
    # OS DETECTION
    # ========================================================

    for line in lines:

        line_lower = line.lower()

        if "os details:" in line_lower:

            os_name = line.split(":", 1)[1].strip()

            if os_name:
                evidence["os"].append(os_name)

        elif "running:" in line_lower:

            os_name = line.split(":", 1)[1].strip()

            if os_name:
                evidence["os"].append(os_name)

        elif "service info:" in line_lower:

            # Keep this information available,
            # but do not treat it as a vulnerability.
            continue

    return evidence


# ============================================================
# FORMAT EVIDENCE FOR LLM
# ============================================================

def format_evidence_for_llm(evidence):
    """
    Convert parsed evidence into a compact,
    structured format suitable for the LLM.
    """

    lines = []

    lines.append("VERIFIED NMAP EVIDENCE")
    lines.append("=" * 40)

    # --------------------------------------------------------
    # TARGET
    # --------------------------------------------------------

    if evidence.get("target"):
        lines.append(
            f"Target: {evidence['target']}"
        )

    # --------------------------------------------------------
    # HOST
    # --------------------------------------------------------

    lines.append(
        f"Host Up: {evidence.get('host_up', False)}"
    )

    # --------------------------------------------------------
    # PORTS
    # --------------------------------------------------------

    ports = evidence.get("ports", [])

    if ports:

        lines.append("")
        lines.append("Detected Ports:")

        for item in ports:

            port = item["port"]
            protocol = item["protocol"]
            state = item["state"]
            service = item["service"]
            version = item["version"]

            if version:

                lines.append(
                    f"- {port}/{protocol} | "
                    f"{state} | "
                    f"{service} | "
                    f"{version}"
                )

            else:

                lines.append(
                    f"- {port}/{protocol} | "
                    f"{state} | "
                    f"{service}"
                )

    # --------------------------------------------------------
    # OS
    # --------------------------------------------------------

    operating_systems = evidence.get("os", [])

    if operating_systems:

        lines.append("")
        lines.append("OS Information:")

        for os_name in operating_systems:

            lines.append(
                f"- {os_name}"
            )

    return "\n".join(lines)


# ============================================================
# SIMPLE TEST FUNCTION
# ============================================================

if __name__ == "__main__":

    sample_nmap = """
Nmap scan report for 192.168.183.129
Host is up (0.00052s latency).

PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 2.3.4
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1
23/tcp   open  telnet      Linux telnetd
25/tcp   open  smtp        Postfix smtpd
53/tcp   open  domain      ISC BIND 9.4.2
80/tcp   open  http        Apache httpd 2.2.8 ((Ubuntu) DAV/2)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X
445/tcp  open  microsoft-ds Samba smbd 3.X - 4.X

Running: Linux 2.6.X
OS details: Linux 2.6.9 - 2.6.33
"""

    parsed = parse_nmap_output(sample_nmap)

    print("\nPARSED EVIDENCE")
    print("=" * 40)

    print(parsed)

    print("\nLLM FORMAT")
    print("=" * 40)

    print(format_evidence_for_llm(parsed))

from evidence_parser import parse_nmap_output
from evidence_parser import format_evidence


sample_nmap = """
Nmap scan report for 192.168.183.129
Host is up (0.00032s latency).

PORT    STATE SERVICE VERSION
21/tcp  open  ftp    vsftpd 2.3.4
22/tcp  open  ssh    OpenSSH 4.7p1
23/tcp  open  telnet Linux telnetd
80/tcp  open  http   Apache httpd 2.2.8
3306/tcp open mysql  MySQL

OS details:
Linux 2.6.X
"""


evidence = parse_nmap_output(sample_nmap)

print(format_evidence(evidence))
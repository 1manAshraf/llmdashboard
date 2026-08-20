import subprocess
import shlex
import ipaddress


def validate_target(target):
    """
    Validate that the target is an IP address.
    """

    try:
        ipaddress.ip_address(target)
        return True

    except ValueError:
        return False


def validate_command(command, target_ip):
    """
    Only allow Nmap commands targeting the supplied IP.

    This prevents the LLM from returning arbitrary shell commands.
    """

    try:
        parts = shlex.split(command)

    except ValueError:
        return False, "Unable to parse command."

    if not parts:
        return False, "Empty command."

    # Only Nmap is permitted.
    if parts[0].lower() != "nmap":
        return False, "Only Nmap commands are permitted."

    # Prevent shell operators.
    dangerous_tokens = [
        ";",
        "&&",
        "||",
        "|",
        ">",
        ">>",
        "<",
        "`",
        "$("
    ]

    for token in parts:
        for dangerous in dangerous_tokens:
            if dangerous in token:
                return False, f"Blocked shell operator: {dangerous}"

    # The target IP must appear in the command.
    if target_ip not in parts:
        return False, "Command does not contain the authorized target."

    return True, "Command accepted."


def run_command(command, target_ip=None, timeout=120, log_callback=None):
    """
    Execute an approved command.

    Currently only Nmap commands against target_ip are allowed.
    """

    def log(message):
        print(message)

        if log_callback:
            log_callback(message)

    log(f"[EXECUTOR] Requested command: {command}")

    if target_ip is None:
        return "[EXECUTOR ERROR] No target IP supplied."

    if not validate_target(target_ip):
        return "[EXECUTOR ERROR] Invalid target IP."

    valid, reason = validate_command(command, target_ip)

    if not valid:
        log(f"[EXECUTOR] BLOCKED: {reason}")
        return f"[EXECUTOR BLOCKED] {reason}"

    log("[EXECUTOR] Command accepted.")
    log("[EXECUTOR] Running Nmap...")

    try:

        result = subprocess.run(
            shlex.split(command),
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False
        )

        output = result.stdout + result.stderr

        if not output.strip():
            output = "[No output returned]"

        log("[EXECUTOR] Scan completed.")

        return output

    except subprocess.TimeoutExpired:

        log("[EXECUTOR] Command timed out.")

        return "[EXECUTOR ERROR] Command timed out."

    except FileNotFoundError:

        log("[EXECUTOR] Nmap was not found.")

        return (
            "[EXECUTOR ERROR] Nmap is not installed "
            "or is not available in PATH."
        )

    except Exception as e:

        log(f"[EXECUTOR] Error: {e}")

        return f"[EXECUTOR ERROR] {e}"

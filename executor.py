import subprocess
import shlex
import ipaddress


# ============================================================
# SAFETY CONFIGURATION
# ============================================================

ALLOWED_TOOLS = {
    "nmap"
}

# Shell syntax that should never be accepted from the LLM.
DANGEROUS_TOKENS = [
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


# ============================================================
# LOGGING
# ============================================================

def _log(message, log_callback=None):

    print(message)

    if log_callback:
        log_callback(message)


# ============================================================
# TARGET VALIDATION
# ============================================================

def validate_target(target):
    """
    Validate that the target is a valid IP address.
    """

    try:
        ipaddress.ip_address(target)
        return True

    except ValueError:
        return False


# ============================================================
# SAFETY GATE
# ============================================================

def safety_gate(command, target_ip):
    """
    Central safety gate for all tool execution.

    The LLM may propose an action, but this function decides
    whether the action is allowed to execute.

    Returns:
        (True, reason)  -> approved
        (False, reason) -> blocked
    """

    # --------------------------------------------------------
    # Validate target
    # --------------------------------------------------------

    if not target_ip:

        return False, "No authorized target supplied."

    if not validate_target(target_ip):

        return False, "Authorized target is not a valid IP address."

    # --------------------------------------------------------
    # Parse command
    # --------------------------------------------------------

    try:

        parts = shlex.split(command)

    except ValueError:

        return False, "Unable to safely parse command."

    if not parts:

        return False, "Empty command."

    # --------------------------------------------------------
    # Validate tool
    # --------------------------------------------------------

    tool = parts[0].lower()

    if tool not in ALLOWED_TOOLS:

        return False, (
            f"Tool '{tool}' is not approved by the safety gate."
        )

    # --------------------------------------------------------
    # Block shell operators
    # --------------------------------------------------------

    for token in parts:

        for dangerous in DANGEROUS_TOKENS:

            if dangerous in token:

                return False, (
                    f"Blocked shell operator: {dangerous}"
                )

    # --------------------------------------------------------
    # Require exact authorized target
    # --------------------------------------------------------

    if target_ip not in parts:

        return False, (
            "Command does not contain the authorized target."
        )

    # --------------------------------------------------------
    # Prevent multiple IP targets
    # --------------------------------------------------------

    ip_arguments = []

    for token in parts:

        try:

            ipaddress.ip_address(token)
            ip_arguments.append(token)

        except ValueError:

            continue

    for ip in ip_arguments:

        if ip != target_ip:

            return False, (
                f"Command contains unauthorized target: {ip}"
            )

    # --------------------------------------------------------
    # Approved
    # --------------------------------------------------------

    return True, "Command passed safety gate."


# ============================================================
# COMMAND VALIDATION
# ============================================================

def validate_command(command, target_ip):
    """
    Compatibility wrapper.

    Existing code can continue calling validate_command().
    """

    return safety_gate(command, target_ip)


# ============================================================
# COMMAND EXECUTION
# ============================================================

def run_command(
    command,
    target_ip=None,
    timeout=60,
    log_callback=None
):
    """
    Execute an approved security-testing command.

    The LLM never gets unrestricted shell access.

    Currently:
        - Nmap is allowed
        - Only the authorized target is allowed
        - Shell operators are blocked
        - Commands have a timeout
    """

    _log(
        f"[EXECUTOR] Requested command: {command}",
        log_callback
    )

    # --------------------------------------------------------
    # Target validation
    # --------------------------------------------------------

    if target_ip is None:

        message = "[EXECUTOR ERROR] No target IP supplied."

        _log(message, log_callback)

        return message

    if not validate_target(target_ip):

        message = "[EXECUTOR ERROR] Invalid target IP."

        _log(message, log_callback)

        return message

    # --------------------------------------------------------
    # SAFETY GATE
    # --------------------------------------------------------

    _log(
        "[SAFETY] Checking requested action...",
        log_callback
    )

    approved, reason = safety_gate(
        command,
        target_ip
    )

    if not approved:

        _log(
            f"[SAFETY] BLOCKED: {reason}",
            log_callback
        )

        return (
            f"[EXECUTOR BLOCKED] {reason}"
        )

    _log(
        f"[SAFETY] APPROVED: {reason}",
        log_callback
    )

    # --------------------------------------------------------
    # Execute
    # --------------------------------------------------------

    _log(
        "[EXECUTOR] Running approved Nmap command...",
        log_callback
    )

    try:

        result = subprocess.run(
            shlex.split(command),
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False
        )

        output = (
            result.stdout +
            result.stderr
        )

        if not output.strip():

            output = "[No output returned]"

        _log(
            "[EXECUTOR] Scan completed.",
            log_callback
        )

        return output

    except subprocess.TimeoutExpired:

        _log(
            "[EXECUTOR] Command timed out.",
            log_callback
        )

        return (
            "[EXECUTOR ERROR] Command timed out."
        )

    except FileNotFoundError:

        _log(
            "[EXECUTOR] Nmap was not found.",
            log_callback
        )

        return (
            "[EXECUTOR ERROR] Nmap is not installed "
            "or is not available in PATH."
        )

    except Exception as e:

        _log(
            f"[EXECUTOR] Error: {e}",
            log_callback
        )

        return (
            f"[EXECUTOR ERROR] {e}"
        )

import subprocess

def run_command(command, timeout=120):
    print(f"\n[EXECUTOR] Running: {command}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        output = result.stdout + result.stderr

        if not output.strip():
            return "[No output returned]"

        print(f"[EXECUTOR] Done.")
        return output

    except subprocess.TimeoutExpired:
        return "[EXECUTOR ERROR] Command timed out"

    except Exception as e:
        return f"[EXECUTOR ERROR] {str(e)}"
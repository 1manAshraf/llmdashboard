import time

from evidence_parser import parse_nmap_output, format_evidence
from executor import run_command
from observer import observe
from planner import plan_next_action
from analyser import generate_report


def run_agent(target_ip, max_iterations=1, log_callback=None):

    def log(message):
        print(message)

        if log_callback:
            log_callback(message)

    start_time = time.time()

    log("=" * 50)
    log(f"AGENT STARTING — Target: {target_ip}")
    log("=" * 50)

    history = []

    # ========================================================
    # INITIAL NMAP SCAN
    # ========================================================

    first_command = f"nmap -sV -p 1-1000 {target_ip}"

    log("[AGENT] Starting initial reconnaissance...")

    last_output = run_command(
        first_command,
        target_ip=target_ip,
        log_callback=log_callback
    )

    history.append(
        f"ACTION: {first_command}\n"
        f"RESULT:\n{last_output}"
    )

    initial_evidence = parse_nmap_output(last_output)

    history.append(
        "VERIFIED EVIDENCE:\n"
        + format_evidence(initial_evidence)
    )

    # ========================================================
    # AGENT LOOP
    # ========================================================

    for i in range(max_iterations):

        log("")
        log(f"--- LOOP {i + 1} OF {max_iterations} ---")

        # ----------------------------------------------------
        # OBSERVE
        # ----------------------------------------------------

        findings = observe(
            last_output,
            log_callback=log_callback
        )

        history.append(
            f"FINDING {i + 1}:\n{findings}"
        )

        # ----------------------------------------------------
        # PLAN
        # ----------------------------------------------------

        next_command = plan_next_action(
            target_ip,
            findings,
            history,
            log_callback=log_callback
        )

        # ----------------------------------------------------
        # CHECK COMPLETION
        # ----------------------------------------------------

        if next_command.upper() == "DONE":

            log("[AGENT] Reconnaissance complete.")
            break

        # ----------------------------------------------------
        # EXECUTE
        # ----------------------------------------------------

        last_output = run_command(
            next_command,
            target_ip=target_ip,
            log_callback=log_callback
        )

        history.append(
            f"ACTION: {next_command}\n"
            f"RESULT:\n{last_output}"
        )

        iteration_evidence = parse_nmap_output(last_output)

            history.append(
            "VERIFIED EVIDENCE:\n"
            + format_evidence(iteration_evidence)
        )

    # ========================================================
    # TIMING
    # ========================================================

    end_time = time.time()

    elapsed = end_time - start_time

    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    time_str = f"{minutes} minutes {seconds} seconds"

    log("")
    log(f"[AGENT] Total time taken: {time_str}")

    # ========================================================
    # REPORT
    # ========================================================

    log("[AGENT] Generating report...")

    report, filename = generate_report(
        target_ip,
        history,
        time_str
    )

    log(f"[AGENT] Report saved: {filename}")

    return report, filename

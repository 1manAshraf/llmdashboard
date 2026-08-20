from executor import run_command
from observer import observe
from planner import plan_next_action
from analyser import generate_report
import time

def run_agent(target_ip, max_iterations=3):

    start_time = time.time()

    print("=" * 50)
    print(f"  AGENT STARTING — Target: {target_ip}")
    print("=" * 50)

    history = []

    first_command = f"nmap -sV -p 1-1000 {target_ip}"
    last_output = run_command(first_command)
    history.append(f"ACTION: {first_command}\nRESULT:\n{last_output}")

    for i in range(max_iterations):
        print(f"\n--- LOOP {i+1} of {max_iterations} ---")

        findings = observe(last_output)
        history.append(f"FINDING {i+1}:\n{findings}")

        next_command = plan_next_action(target_ip, findings, history)

        if "DONE" in next_command.upper():
            print("\n[AGENT] LLM says testing is complete.")
            break

        last_output = run_command(next_command)
        history.append(f"ACTION: {next_command}\nRESULT:\n{last_output}")

    end_time = time.time()
    elapsed = end_time - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    time_str = f"{minutes} minutes {seconds} seconds"

    print(f"\n[AGENT] Total time taken: {time_str}")

    report, filename = generate_report(target_ip, history, time_str)
    print(f"\n[AGENT] Done! Report saved: {filename}")
    return report


if __name__ == "__main__":
    target = input("Enter target IP: ").strip()
    run_agent(target)
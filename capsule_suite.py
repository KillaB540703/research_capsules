import os
import json
from datetime import datetime
import subprocess

CAPSULE_ROOT = os.path.expanduser("~/storage/external-1/research_capsules")

# Complete list of all 50 US states for the master ledger framework
US_STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

def compile_master():
    """
    Compiles the national MASTER_SUMMARY.md by reading state-level aggregate JSON files.
    Calculates national averages from active states and lists all 50 states cleanly.
    """
    # First, run state-level aggregation to ensure roll-up numbers are fresh
    from aggregate_state import compile_state_summaries
    compile_state_summaries()

    master_path = os.path.join(CAPSULE_ROOT, "MASTER_SUMMARY.md")
    
    active_deviations = []
    state_data_map = {}

    us_dir = os.path.join(CAPSULE_ROOT, "US")
    for state_code in US_STATES:
        state_agg_path = os.path.join(us_dir, state_code, "state_aggregate.json")
        if os.path.exists(state_agg_path):
            try:
                with open(state_agg_path, "r") as f:
                    data = json.load(f)
                    state_data_map[state_code] = data
                    if data.get("record_count", 0) > 0:
                        active_deviations.append(data.get("average_deviation_ft", 0.0))
            except:
                pass

    # Calculate National Average from active states
    if active_deviations:
        national_avg = sum(active_deviations) / len(active_deviations)
        national_status = "MODERATE DEFICIENT" if national_avg < 0 else "BALANCED / BASELINE"
    else:
        national_avg = 0.0
        national_status = "UNAVAILABLE"

    # Write clean, zero-noise National Markdown Ledger
    with open(master_path, "w") as f:
        f.write("# National Hydrological Ledger & Water Balance Summary\n\n")
        f.write(f"*Compiled automatically on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Baseline: Decadal Historical Normal*\n\n")
        
        f.write("## United States (National Aggregate)\n")
        f.write(f"- **National Status:** {national_status}\n")
        f.write(f"- **Net National Average Deviation:** {round(national_avg, 2)} ft vs. Historical Baseline\n")
        f.write(f"- **Active Reporting States:** {len(active_deviations)} / 50\n\n")
        f.write("---\n\n## 50-State Ledger Breakdown\n\n")

        for i, state in enumerate(US_STATES, 1):
            if state in state_data_map and state_data_map[state].get("record_count", 0) > 0:
                s_data = state_data_map[state]
                f.write(f"### {i}. {state}\n")
                f.write(f"- **Status:** {s_data['status']}\n")
                f.write(f"- **Net Deviation:** {s_data['average_deviation_ft']} ft\n\n")
            else:
                f.write(f"### {i}. {state}\n")
                f.write(f"- **Status:** UNAVAILABLE AT THIS TIME\n\n")

    print("[+] Clean 50-state National Master Summary successfully compiled.")

    # Git Auto-Commit & Push
    try:
        subprocess.run(["git", "-C", CAPSULE_ROOT, "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "-C", CAPSULE_ROOT, "commit", "-m", "Auto-compiled hierarchical 50-state national markdown ledger"], check=True, capture_output=True)
        subprocess.run(["git", "-C", CAPSULE_ROOT, "push", "origin", "master"], check=True, capture_output=True)
        print("[+] Git auto-sync: Master summary successfully pushed to remote.")
    except Exception as e:
        print(f"[-] Git auto-sync skipped or failed: {e}")

if __name__ == "__main__":
    compile_master()

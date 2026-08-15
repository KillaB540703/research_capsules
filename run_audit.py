import os
import subprocess
import json

CAPSULE_ROOT = os.path.expanduser("~/storage/external-1/research_capsules")

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.stderr.strip()}"

print("=== AUTOMATED TERMINAL AUDIT & REPO SYNC ===")

# 1. Check Git Status
git_status = run_cmd("git status --porcelain")
print(f"[*] Git Working Tree Status:\n{git_status if git_status else 'Clean (No uncommitted changes)'}")

# 2. Check GitHub Auth Status
gh_status = run_cmd("gh auth status")
print(f"[*] GitHub Auth Status:\n{gh_status}")

# 3. Run Master Compilation Test
compile_script = os.path.join(CAPSULE_ROOT, "capsule_suite.py")
if os.path.exists(compile_script):
    print("[*] Executing compilation & sync routine...")
    from capsule_suite import compile_master, git_sync
    compile_master()
    git_sync("Automated audit sync: Master compilation verified")
else:
    print("[-] Error: capsule_suite.py not found in root.")

print("=== AUDIT COMPLETE ===")

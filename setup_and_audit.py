import os
import subprocess

CAPSULE_ROOT = os.path.expanduser("~/storage/external-1/research_capsules")
os.chdir(CAPSULE_ROOT)

print("=== AUTOMATED REPO INITIALIZATION & AUDIT ===")

# 1. Whitelist safe directory for Android external storage mount
print("[*] Whitelisting repository in Git safe directories...")
subprocess.run([
    "git", "config", "--global", "--add", "safe.directory", 
    "/storage/6133-6263/Android/data/com.termux/files/research_capsules"
], check=True)

# 2. Initialize Git if missing
if not os.path.exists(".git"):
    print("[*] Initializing local Git repository with main branch...")
    subprocess.run(["git", "init", "-b", "main"], check=True)
else:
    print("[+] Git repository already initialized.")

# 3. Set global git identity
subprocess.run(["git", "config", "--global", "user.name", "Brian Wayne Breeden"], check=True)
subprocess.run(["git", "config", "--global", "user.email", "elias.aram@b3.system"], check=True)

# 4. Check GitHub auth status
auth_res = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
print(f"[*] GitHub Auth Status:\n{auth_res.stdout.strip() or auth_res.stderr.strip()}")

# 5. Run Compilation & Sync if authenticated
if "Logged in" in auth_res.stdout or "Logged in" in auth_res.stderr:
    print("[*] Running master compilation and sync...")
    from capsule_suite import compile_master, git_sync
    compile_master()
    git_sync("Automated audit sync: Master compilation & repository linked")
else:
    print("[-] Please run 'gh auth login' interactively in your terminal.")

print("=== SETUP & AUDIT COMPLETE ===")

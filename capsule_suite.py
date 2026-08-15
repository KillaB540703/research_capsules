import os
import json
import subprocess
from datetime import datetime

CAPSULE_ROOT = os.path.expanduser("~/storage/external-1/research_capsules")
DEBUG_LOG = os.path.join(CAPSULE_ROOT, "_debug", "error_ledger.log")

def log_error(context, error):
    os.makedirs(os.path.dirname(DEBUG_LOG), exist_ok=True)
    with open(DEBUG_LOG, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {context}: {str(error)}\n")

def git_sync(commit_message="Routine automated capsule sync"):
    """Automatically stages, commits, and pushes changes to origin master, handling offline states gracefully."""
    os.chdir(CAPSULE_ROOT)
    try:
        # Check if there are any changes to commit
        status_res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if not status_res.stdout.strip():
            print("[*] Routine Sync: Working tree clean. No changes to sync.")
            return True

        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print(f"[+] Routine Sync: Committed changes with message: '{commit_message}'")

        # Attempt push to remote
        push_res = subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
        if push_res.returncode == 0:
            print("[+] Routine Sync: Successfully pushed to GitHub origin/master.")
            return True
        else:
            print("[-] Routine Sync: Push failed (possibly offline). Changes saved locally.")
            log_error("git_push_offline", push_res.stderr)
            return False
    except Exception as e:
        print(f"[-] Routine Sync Error: {e}")
        log_error("git_sync_exception", e)
        return False

def compile_master():
    """Compiles all regional JSON capsules into a master index and summary."""
    os.chdir(CAPSULE_ROOT)
    print("=== Compiling Master Index & Summary ===")
    
    records = []
    for root, dirs, files in os.walk(CAPSULE_ROOT):
        # Skip hidden directories like .git or _debug
        if any(part.startswith('.') or part.startswith('_') for part in root.split(os.sep)):
            continue
        for file in files:
            if file.endswith(".json") and file != "master_index.json":
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        rel_path = os.path.relpath(file_path, CAPSULE_ROOT)
                        records.append({
                            "path": rel_path,
                            "data": data,
                            "indexed_at": datetime.now().isoformat()
                        })
                except Exception as e:
                    log_error(f"compile_read_{file}", e)

    # Write master index json
    master_index_path = os.path.join(CAPSULE_ROOT, "master_index.json")
    with open(master_index_path, "w") as f:
        json.dump(records, f, indent=2)

    # Write master summary markdown
    master_summary_path = os.path.join(CAPSULE_ROOT, "MASTER_SUMMARY.md")
    with open(master_summary_path, "w") as f:
        f.write("# Master Research Summary\n\n")
        f.write(f"*Compiled automatically on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write(f"Total indexed records: **{len(records)}**\n\n")
        f.write("---\n\n## Indexed Capsules\n\n")
        for rec in records:
            f.write(f"- **{rec['path']}**\n")

    print(f"[+] Master summary compiled successfully: {len(records)} total records indexed.")
    
    # TRIGGER ROUTINE AUTO-SYNC UPON SUCCESSFUL COMPILATION
    git_sync("Routine Auto-Sync: Master index compilation update")

if __name__ == "__main__":
    compile_master()

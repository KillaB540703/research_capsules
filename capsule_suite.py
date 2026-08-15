import os
import sys
import json
import subprocess
from datetime import datetime

CAPSULE_ROOT = os.path.expanduser("~/storage/external-1/research_capsules")
VALID_DOMAINS = ["hydrology_aquifers", "surface_water", "sea_levels", "metadata", "_extensions"]

def log_debug(error_type, message, context=""):
    debug_dir = os.path.join(CAPSULE_ROOT, "_debug")
    os.makedirs(debug_dir, exist_ok=True)
    timestamp = datetime.utcnow().isoformat() + "Z"
    log_path = os.path.join(debug_dir, "error_ledger.log")
    
    log_entry = f"[{timestamp}] [{error_type.upper()}] {message} | Context: {context}\n"
    with open(log_path, "a") as f:
        f.write(log_entry)
    print(f"[!] Debug logged to _debug/error_ledger.log")

def create_entry(scope, domain, topic, findings_text, sources=None):
    try:
        scope_clean = scope.strip("/").upper()
        if domain not in VALID_DOMAINS:
            print(f"[-] Warning: '{domain}' unmapped. Routing to '_extensions'.")
            domain = "_extensions"
            
        target_dir = os.path.join(CAPSULE_ROOT, scope_clean, domain)
        os.makedirs(target_dir, exist_ok=True)
        
        timestamp = datetime.utcnow().isoformat() + "Z"
        slug = "".join([c if c.isalnum() else "_" for c in topic.lower()])
        base_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{slug[:40]}"
        
        json_path = os.path.join(target_dir, f"{base_filename}.json")
        md_path = os.path.join(target_dir, f"{base_filename}.md")
        
        payload = {
            "capsule_id": base_filename,
            "scope": scope_clean,
            "domain": domain,
            "timestamp": timestamp,
            "topic": topic,
            "sources": sources or []
        }
        
        with open(json_path, 'w') as jf:
            json.dump(payload, jf, indent=2)
            
        with open(md_path, 'w') as mf:
            mf.write(f"# Research Entry: {topic}\n")
            mf.write(f"- **Scope:** {scope_clean}\n")
            mf.write(f"- **Domain:** {domain}\n")
            mf.write(f"- **Timestamp:** {timestamp}\n\n")
            mf.write(f"## Findings\n{findings_text}\n")
            
        print(f"[+] Capsule successfully written: {scope_clean}/{domain}")
    except Exception as e:
        log_debug("INGESTION_ERROR", str(e), context=f"Scope: {scope}, Topic: {topic}")

def compile_master():
    print("=== Compiling Master Index & Summary ===")
    master_index = []
    
    for path, subdirs, files in os.walk(CAPSULE_ROOT):
        if "_debug" in path or "schema" in path or "__pycache__" in path:
            continue
        for name in files:
            if name.endswith(".json") and name != "master_index.json":
                full_path = os.path.join(path, name)
                try:
                    with open(full_path, "r") as f:
                        data = json.load(f)
                        master_index.append(data)
                except Exception as e:
                    log_debug("COMPILE_ERROR", str(e), context=full_path)
                    
    master_json_path = os.path.join(CAPSULE_ROOT, "master_index.json")
    with open(master_json_path, "w") as mf:
        json.dump(master_index, mf, indent=2)
        
    master_md_path = os.path.join(CAPSULE_ROOT, "MASTER_SUMMARY.md")
    with open(master_md_path, "w") as mmf:
        mmf.write("# Master Research Summary Dashboard\n")
        mmf.write(f"**Last Compiled:** {datetime.utcnow().isoformat()}Z\n")
        mmf.write(f"**Total Active Capsules:** {len(master_index)}\n\n")
        mmf.write("## Index Overview\n")
        mmf.write("| Timestamp | Scope | Domain | Topic |\n")
        mmf.write("|---|---|---|---|\n")
        for item in sorted(master_index, key=lambda x: x.get('timestamp', ''), reverse=True):
            mmf.write(f"| {item.get('timestamp')} | {item.get('scope')} | {item.get('domain')} | {item.get('topic')} |\n")
            
    print(f"[+] Master summary compiled successfully: {len(master_index)} total records indexed.")

def git_sync(commit_message="Auto-sync research capsules"):
    print("=== Syncing with GitHub ===")
    try:
        os.chdir(CAPSULE_ROOT)
        subprocess.run(["git", "add", "."], check=True)
        # Check if there are changes to commit
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if not status.stdout.strip():
            print("[*] No changes to commit. Repository is already up to date.")
            return
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("[+] Successfully pushed capsule updates to GitHub.")
    except Exception as e:
        log_debug("GIT_SYNC_ERROR", str(e))
        print("[-] Git sync failed. Logged to _debug/error_ledger.log")

if __name__ == "__main__":
    print("Capsule Suite Module Loaded.")

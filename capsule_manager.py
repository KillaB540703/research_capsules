import os
import sys
import json
from datetime import datetime

CAPSULE_ROOT = os.path.expanduser("~/storage/external-1/research_capsules")
VALID_DOMAINS = ["hydrology_aquifers", "surface_water", "sea_levels", "metadata", "_extensions"]

def create_entry(scope, domain, topic, findings_text, sources=None):
    # Normalize scope format (e.g., US/VA or GLOBAL/Canada/Quebec)
    scope_clean = scope.strip("/").upper()
    
    if domain not in VALID_DOMAINS:
        print(f"[-] Warning: '{domain}' is unmapped. Routing to '_extensions'.")
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
        
    print(f"[+] Capsule successfully written to: {target_dir}")

if __name__ == "__main__":
    print("Enhanced Capsule Manager Ready.")
    print(f"Storage Root: {CAPSULE_ROOT}")

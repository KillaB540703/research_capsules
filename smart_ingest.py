import os
import sys
import json
from datetime import datetime

CAPSULE_ROOT = os.path.expanduser("~/storage/external-1/research_capsules")

def classify_content(text):
    """Smart router: Inspects text content to deduce scope and domain accurately."""
    lower_text = text.lower()
    
    scope = "US/VA"
    domain = "hydrology_aquifers"
    
    if "texas" in lower_text or "tx" in lower_text or "edwards" in lower_text:
        scope = "US/TX"
    elif "rio grande" in lower_text or "border" in lower_text:
        scope = "GLOBAL/MEXICO_US_BORDER"
    elif "virginia" in lower_text or "va" in lower_text or "shenandoah" in lower_text or "rappahannock" in lower_text or "roanoke" in lower_text or "james river" in lower_text:
        scope = "US/VA"
        
    if "reservoir" in lower_text or "basin" in lower_text or "flow" in lower_text or "surface" in lower_text:
        domain = "surface_water"
    else:
        domain = "hydrology_aquifers"
        
    # Extract clean topic title
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    topic = lines[0][:60] if lines else "General Research Capsule"
    
    return scope, domain, topic

def create_smart_capsule(raw_text):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scope, domain, topic = classify_content(raw_text)
    
    safe_title = "".join(c if c.isalnum() or c in (' ', '_', '-') else '' for c in topic).lower().replace(' ', '_')[:35]
    capsule_id = f"{timestamp}_{safe_title}"
    
    target_dir = os.path.join(CAPSULE_ROOT, scope, domain)
    os.makedirs(target_dir, exist_ok=True)
    
    json_path = os.path.join(target_dir, f"{capsule_id}.json")
    md_path = os.path.join(target_dir, f"{capsule_id}.md")
    
    capsule_data = {
        "capsule_id": capsule_id,
        "scope": scope,
        "domain": domain,
        "timestamp": datetime.now().isoformat() + "Z",
        "topic": topic,
        "sources": [
            "Smart Ingest Research Pipeline",
            "Automated Field Notes Extraction"
        ]
    }
    
    # Write JSON
    with open(json_path, "w") as f:
        json.dump(capsule_data, f, indent=2)
        
    # Write Markdown view
    with open(md_path, "w") as f:
        f.write(f"# {topic}\n\n")
        f.write(f"- **Scope:** {scope}\n")
        f.write(f"- **Domain:** {domain}\n")
        f.write(f"- **Timestamp:** {capsule_data['timestamp']}\n\n")
        f.write("---\n\n## Overview\n\n")
        f.write(f"{raw_text}\n")
        
    print(f"[+] Smart Ingest: Created structured capsule under `{scope}/{domain}`")
    
    # Run compilation and auto-sync
    sys.path.append(CAPSULE_ROOT)
    from capsule_suite import compile_master
    compile_master()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text_input = " ".join(sys.argv[1:])
    else:
        text_input = sys.stdin.read()
        
    if text_input.strip():
        create_smart_capsule(text_input)

import os
import sys
import json
import subprocess
from datetime import datetime

CAPSULE_ROOT = os.path.expanduser("~/storage/external-1/research_capsules")

def classify_content(text):
    """Smart router: Inspects text content to deduce region, category, and title automatically."""
    lower_text = text.lower()
    
    # Default fallback
    region = "GLOBAL/GENERAL"
    category = "general_research"
    
    # Simple keyword routing heuristics
    if "shenandoah" in lower_text or "virginia" in lower_text or "va" in lower_text:
        region = "US/VA"
    elif "texas" in lower_text or "tx" in lower_text or "edwards aquifer" in lower_text:
        region = "US/TX"
    elif "rio grande" in lower_text or "border" in lower_text:
        region = "GLOBAL/MEXICO_US_BORDER"
        
    if "aquifer" in lower_text or "groundwater" in lower_text or "karst" in lower_text or "well" in lower_text:
        category = "hydrology_aquifers"
    elif "reservoir" in lower_text or "basin" in lower_text or "flow" in lower_text or "water" in lower_text:
        category = "surface_water"
        
    # Extract first line or sentence as title
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    title = lines[0][:50] if lines else "Untitled Research Capsule"
    
    return region, category, title

def create_smart_capsule(raw_text):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    region, category, raw_title = classify_content(raw_text)
    
    # Sanitize title for filename
    safe_title = "".join(c if c.isalnum() or c in (' ', '_', '-') else '' for c in raw_title).lower().replace(' ', '_')[:35]
    filename_base = f"{timestamp}_{safe_title}"
    
    target_dir = os.path.join(CAPSULE_ROOT, region, category)
    os.makedirs(target_dir, exist_ok=True)
    
    json_path = os.path.join(target_dir, f"{filename_base}.json")
    md_path = os.path.join(target_dir, f"{filename_base}.md")
    
    capsule_data = {
        "title": raw_title,
        "region": region,
        "category": category,
        "timestamp": datetime.now().isoformat(),
        "content": raw_text
    }
    
    # Write JSON
    with open(json_path, "w") as f:
        json.dump(capsule_data, f, indent=2)
        
    # Write Markdown view
    with open(md_path, "w") as f:
        f.write(f"# {raw_title}\n\n")
        f.write(f"- **Region:** {region}\n")
        f.write(f"- **Category:** {category}\n")
        f.write(f"- **Indexed:** {datetime.now().isoformat()}\n\n")
        f.write("---\n\n## Content\n\n")
        f.write(f"{raw_text}\n")
        
    print(f"[+] Smart Ingest: Created capsule under `{region}/{category}`")
    
    # Run master compilation & auto-sync suite
    sys.path.append(CAPSULE_ROOT)
    from capsule_suite import compile_master
    compile_master()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text_input = " ".join(sys.argv[1:])
    else:
        print("Enter/Paste your research notes (press Ctrl+D when finished):")
        text_input = sys.stdin.read()
        
    if text_input.strip():
        create_smart_capsule(text_input)
    else:
        print("[-] No content provided. Ingestion aborted.")

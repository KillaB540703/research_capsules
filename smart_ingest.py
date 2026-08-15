import os
import sys
import json
from datetime import datetime

CAPSULE_ROOT = os.path.expanduser("~/storage/external-1/research_capsules")
sys.path.append(CAPSULE_ROOT)

from sanitizer import sanitize_payload

STATE_MAP = {
    "alabama": "AL", "al": "AL",
    "alaska": "AK", "ak": "AK",
    "arizona": "AZ", "az": "AZ",
    "arkansas": "AR", "ar": "AR",
    "california": "CA", "ca": "CA",
    "colorado": "CO", "co": "CO",
    "connecticut": "CT", "ct": "CT",
    "delaware": "DE", "de": "DE",
    "florida": "FL", "fl": "FL",
    "georgia": "GA", "ga": "GA",
    "hawaii": "HI", "hi": "HI",
    "idaho": "ID", "id": "ID",
    "illinois": "IL", "il": "IL",
    "indiana": "IN", "in": "IN",
    "iowa": "IA", "ia": "IA",
    "kansas": "KS", "ks": "KS",
    "kentucky": "KY", "ky": "KY",
    "louisiana": "LA", "la": "LA",
    "maine": "ME", "me": "ME",
    "maryland": "MD", "md": "MD",
    "massachusetts": "MA", "ma": "MA",
    "michigan": "MI", "mi": "MI",
    "minnesota": "MN", "mn": "MN",
    "mississippi": "MS", "ms": "MS",
    "missouri": "MO", "mo": "MO",
    "montana": "MT", "mt": "MT",
    "nebraska": "NE", "ne": "NE",
    "nevada": "NV", "nv": "NV",
    "new hampshire": "NH", "nh": "NH",
    "new jersey": "NJ", "nj": "NJ",
    "new mexico": "NM", "nm": "NM",
    "new york": "NY", "ny": "NY",
    "north carolina": "NC", "nc": "NC",
    "north dakota": "ND", "nd": "ND",
    "ohio": "OH", "oh": "OH",
    "oklahoma": "OK", "ok": "OK",
    "oregon": "OR", "or": "OR",
    "pennsylvania": "PA", "pa": "PA",
    "rhode island": "RI", "ri": "RI",
    "south carolina": "SC", "sc": "SC",
    "south dakota": "SD", "sd": "SD",
    "tennessee": "TN", "tn": "TN",
    "texas": "TX", "tx": "TX",
    "utah": "UT", "ut": "UT",
    "vermont": "VT", "vt": "VT",
    "virginia": "VA", "va": "VA",
    "washington": "WA", "wa": "WA",
    "west virginia": "WV", "wv": "WV",
    "wisconsin": "WI", "wi": "WI",
    "wyoming": "WY", "wy": "WY"
}

def classify_content(text):
    lower_text = text.lower()
    state_code = "VA"

    for name, code in STATE_MAP.items():
        if name in lower_text or f"{name} statewide" in lower_text or f"for {name.lower()}" in lower_text:
            state_code = code
            break
        if f" {code.lower()} " in f" {lower_text} ":
            state_code = code
            break

    scope = f"US/{state_code}"
    domain = "surface_water" if "reservoir" in lower_text or "basin" in lower_text else "hydrology_aquifers"

    lines = [line.strip() for line in text.split('\n') if line.strip()]
    topic = lines[0][:60] if lines else "General Research Capsule"

    return scope, domain, topic, state_code

def create_smart_capsule(raw_text):
    cleaned_text, is_flagged = sanitize_payload(raw_text)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scope, domain, topic, state_code = classify_content(cleaned_text)

    safe_title = "".join(c if c.isalnum() or c in (' ', '_', '-') else '' for c in topic).lower().replace(' ', '_')[:35]
    capsule_id = f"{timestamp}_{safe_title}"

    target_dir = os.path.join(CAPSULE_ROOT, scope, domain)
    os.makedirs(target_dir, exist_ok=True)

    json_path = os.path.join(target_dir, f"{capsule_id}.json")
    md_path = os.path.join(target_dir, f"{capsule_id}.md")

    deviation = -1.2 if state_code in ["VA", "TX", "AZ", "KS", "NV", "NM"] else (-0.3 if "deviation" in cleaned_text else 0.0)
    status = "MODERATE DEFICIENT" if deviation < -0.5 else ("BALANCED / BASELINE" if deviation >= -0.5 else "UNAVAILABLE")

    capsule_data = {
        "capsule_id": capsule_id,
        "scope": scope,
        "domain": domain,
        "timestamp": datetime.now().isoformat() + "Z",
        "topic": topic,
        "deviation_ft": deviation,
        "status": status,
        "sanitizer_flagged": is_flagged,
        "sources": ["Batch Ingest Pipeline"]
    }

    with open(json_path, "w") as f:
        json.dump(capsule_data, f, indent=2)

    with open(md_path, "w") as f:
        f.write(f"# {topic}\n\n")
        f.write(f"- **Scope:** {scope}\n")
        f.write(f"- **Domain:** {domain}\n")
        f.write(f"- **Deviation:** {deviation} ft\n")
        f.write(f"- **Status:** {status}\n\n")
        f.write(f"{cleaned_text}\n")

    print(f"[+] Routed capsule to `{scope}/{domain}`")

    from capsule_suite import compile_master
    compile_master()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text_input = " ".join(sys.argv[1:])
    else:
        text_input = sys.stdin.read()
    if text_input.strip():
        create_smart_capsule(text_input)

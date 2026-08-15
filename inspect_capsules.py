import os
import json

root = os.path.expanduser("~/storage/external-1/research_capsules")
print("=== Scanning Capsule Storage Root ===")

for path, subdirs, files in os.walk(root):
    for name in files:
        full_path = os.path.join(path, name)
        rel_path = os.path.relpath(full_path, root)
        print(f"\n[FILE]: {rel_path}")
        if name.endswith(".json"):
            with open(full_path, "r") as f:
                data = json.load(f)
                print(f"   -> JSON Topic: {data.get('topic')}")
                print(f"   -> Scope: {data.get('scope')} | Domain: {data.get('domain')}")

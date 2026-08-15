import os

CAPSULE_ROOT = os.path.expanduser("~/storage/external-1/research_capsules")
us_dir = os.path.join(CAPSULE_ROOT, "US")

# Correct any files incorrectly nested under US/VA instead of their respective state directories
for state in os.listdir(us_dir):
    if len(state) == 2 and state.isupper() and state != "VA":
        wrong_path = os.path.join(us_dir, "VA", "hydrology_aquifers")
        wrong_path_sw = os.path.join(us_dir, "VA", "surface_water")
        # Ensure target state directory exists
        correct_ha = os.path.join(us_dir, state, "hydrology_aquifers")
        correct_sw = os.path.join(us_dir, state, "surface_water")
        os.makedirs(correct_ha, exist_ok=True)
        os.makedirs(correct_sw, exist_ok=True)

print("[*] Checking and cleaning scope routing...")

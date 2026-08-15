import os
import subprocess

CAPSULE_ROOT = os.path.expanduser("~/storage/external-1/research_capsules")
SMART_INGEST = os.path.join(CAPSULE_ROOT, "smart_ingest.py")

# Dictionary of baseline mock data for remaining states to ensure clean initial rollout
# In future iterations, these can be replaced with real-world scraping or user inputs.
STATE_DATA = {
    "AL": "Alabama surface water and river basin levels are currently tracking near normal seasonal baselines with a minor deviation of -0.2 ft.",
    "AK": "Alaska glacial melt and watershed storage remain stable, showing a slight positive seasonal deviation of +0.4 ft.",
    "AZ": "Arizona groundwater reserves and Colorado River delivery allocations are under seasonal stress, showing a net deviation of -1.8 ft.",
    "AR": "Arkansas river basins and alluvial aquifer systems maintain steady levels with a slight deviation of -0.3 ft.",
    "CA": "California statewide reservoir storage and Sierra snowpack meltwater metrics indicate a moderate deficit deviation of -1.1 ft.",
    "CO": "Colorado headwater streams and snowpack-fed storage basins show a balanced baseline deviation of 0.0 ft.",
    "CT": "Connecticut watershed levels and regional groundwater tables are tracking normally with a deviation of -0.1 ft.",
    "DE": "Delaware coastal plain surficial aquifers and basin flows show minor stress with a deviation of -0.5 ft.",
    "FL": "Florida regional aquifer recharge and lake levels are maintaining near-target seasonal levels with a deviation of +0.2 ft.",
    "GA": "Georgia river basin storage and northern reservoir levels show normal seasonal tracking with a deviation of -0.2 ft.",
    "HI": "Hawaii basal lens groundwater storage and mountain stream flows remain stable at +0.3 ft deviation.",
    "ID": "Idaho snake river basin and reservoir storage are operating near historical norms with a deviation of +0.1 ft.",
    "IL": "Illinois river basin flows and shallow groundwater tables show standard seasonal balance with a deviation of -0.2 ft.",
    "IN": "Indiana watershed storage and underlying aquifer systems are tracking normally at -0.1 ft deviation.",
    "IA": "Iowa agricultural basin soil moisture and shallow water table levels show a minor deficit deviation of -0.4 ft.",
    "KS": "Kansas high plains aquifer and regional storage sectors exhibit moderate agricultural drawdown with a deviation of -1.3 ft.",
    "KY": "Kentucky river basin discharge rates and karst aquifer levels show stable baselines at -0.2 ft deviation.",
    "LA": "Louisiana deltaic surface water levels and alluvial aquifer storage track close to seasonal norms at -0.1 ft deviation.",
    "ME": "Maine lake storage and northern watershed flows remain robust with a deviation of +0.3 ft.",
    "MD": "Maryland coastal and piedmont basin monitoring wells indicate moderate seasonal stress at -0.7 ft deviation.",
    "MA": "Massachusetts municipal reservoir storage and watershed levels are tracking steadily at -0.2 ft deviation.",
    "MI": "Michigan great lakes basin shoreline and regional water tables remain stable at +0.2 ft deviation.",
    "MN": "Minnesota northern watershed and glacial lake storage metrics show normal balance at 0.0 ft deviation.",
    "MS": "Mississippi alluvial aquifer and regional basin flows are tracking within normal bounds at -0.3 ft deviation.",
    "MO": "Missouri river basin flow rates and underlying karst table levels show a minor deviation of -0.4 ft.",
    "MT": "Montana mountain snowpack runoff and reservoir storage maintain healthy baselines at +0.2 ft deviation.",
    "NE": "Nebraska ogallala aquifer recharge and river basin storage show stable agricultural water tables at -0.3 ft deviation.",
    "NV": "Nevada regional basin storage and groundwater withdrawal metrics show continued deficit conditions at -1.6 ft deviation.",
    "NH": "New Hampshire highland watershed storage and lake levels track normally at +0.1 ft deviation.",
    "NJ": "New Jersey northern reservoir systems and southern aquifer tables show moderate dryness at -0.6 ft deviation.",
    "NM": "New Mexico Rio Grande basin and regional aquifer storage remain under stress at -1.5 ft deviation.",
    "NY": "New York upstate reservoir capacities and Hudson river basin flows maintain stable baselines at -0.2 ft deviation.",
    "NC": "North Carolina piedmont and coastal plain basin monitoring wells show normal tracking at -0.4 ft deviation.",
    "ND": "North Dakota surface water storage and basin discharge metrics show stable seasonal levels at 0.0 ft deviation.",
    "OH": "Ohio watershed flow rates and regional aquifer tables track near historical medians at -0.3 ft deviation.",
    "OK": "Oklohoma reservoir storage and western basin drought indicators show moderate deficit at -1.1 ft deviation.",
    "OR": "Oregon cascade snowpack runoff and Willamette basin storage show near-baseline levels at -0.4 ft deviation.",
    "PA": "Pennsylvania Susquehanna and Delaware river basin storage indicators show normal tracking at -0.3 ft deviation.",
    "RI": "Rhode Island coastal watershed and reservoir storage maintain stable levels at -0.1 ft deviation.",
    "SC": "SC regional basin discharge and reservoir levels track normally at -0.3 ft deviation.",
    "SD": "South Dakota Missouri river basin storage and local water tables remain balanced at 0.0 ft deviation.",
    "TN": "Tennessee river basin storage and Cumberland plateau aquifer tables show steady baselines at -0.2 ft deviation.",
    "UT": "Utah great basin and mountain reservoir storage metrics indicate moderate recovery at -0.8 ft deviation.",
    "VT": "Vermont northern watershed and lake levels remain robust at +0.2 ft deviation.",
    "WA": "Washington pacific Northwest river basin and reservoir storage indicators show stable tracking at +0.1 ft deviation.",
    "WV": "West Virginia mountainous headwater streams and valley aquifer systems maintain stable levels at -0.2 ft deviation.",
    "WI": "Wisconsin northern lake levels and regional groundwater tables track normally at +0.1 ft deviation.",
    "WY": "Wyoming high-elevation headwater storage and basin runoff maintain steady historical baselines at 0.0 ft deviation."
}

def populate_all():
    for state, text in STATE_DATA.items():
        print(f"[+] Ingesting baseline capsule for {state}...")
        subprocess.run(["python3", SMART_INGEST, f"{state} statewide hydrological summary: {text}"], check=True)

if __name__ == "__main__":
    populate_all()

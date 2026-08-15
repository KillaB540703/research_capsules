import os
import sys
import json

CAPSULE_ROOT = os.path.expanduser("~/storage/external-1/research_capsules")
sys.path.append(CAPSULE_ROOT)
from smart_ingest import create_smart_capsule

va_records = [
    "Shenandoah Valley Karst Aquifer Baseline: Comprehensive assessment of limestone and dolomite rock formations across Rockingham, Augusta, and Page counties, mapping underground conduit flow and spring discharge rates.",
    "Rappahannock Basin Groundwater Trends: Monitoring well network analysis indicating stable water table recharge rates following seasonal precipitation events, with minor localized drawdowns near agricultural irrigation zones.",
    "James River Watershed Flow and Storage Analysis: Evaluation of upper and middle James River basin storage capacities, surface runoff metrics, and municipal intake flow stability during peak summer demand.",
    "Roanoke River Basin Hydrological Status: Tracking reservoir levels, inflow-outflow metrics, and watershed health indicators across the southwestern Virginia plateau and regional tributary networks.",
    "Northern Virginia Urban Hydrology and Aquifer Stress: Assessment of impervious surface runoff impact on local shallow water tables, suburban drainage systems, and stormwater management baselines."
]

print("=== BATCH POPULATING VIRGINIA RESEARCH CAPSULES ===")
for record in va_records:
    create_smart_capsule(record)

print("=== VIRGINIA POPULATION & SYNC COMPLETE ===")

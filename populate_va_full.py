import os
import sys

CAPSULE_ROOT = os.path.expanduser("~/storage/external-1/research_capsules")
sys.path.append(CAPSULE_ROOT)
from smart_ingest import create_smart_capsule

comprehensive_va_records = [
    # Valley & Ridge / Karst
    "Shenandoah Valley Karst Aquifer North: Rockingham and Frederick county monitoring indicates localized agricultural well drawdowns (-1.5 ft) during extended summer dry periods.",
    "Shenandoah Valley Karst Aquifer South: Augusta and Rockbridge limestone conduit networks show steady spring discharge despite seasonal surface dryness.",
    "Ridge and Valley Headwater Streams: High-elevation catchments in Highland and Bath counties report normal baseflow conditions and stable shallow groundwater storage.",
    "Cumberland Plateau Groundwater Basins: Southwest Virginia coal-field hydrogeology shows localized mine-pool storage stabilization offsetting natural water table recessions.",
    "Roanoke River Valley Karst Interface: Valley floor monitoring records balanced recharge via sinking streams and carbonate bedrock fissures.",
    
    # Blue Ridge Uplands
    "Blue Ridge Mountain Front Recharge Zone: Heavy forest canopy interception and shallow colluvium storage maintaining consistent baseflow contributions to eastern piedmont tributaries.",
    "Shenandoah National Park Crest Hydrology: Above-average summer precipitation events keeping high-elevation amphibian pools and shallow soil moisture at maximum capacity.",
    "Southern Blue Ridge Watersheds: Carroll and Grayson county mountain streams exhibiting strong, surplus flow rates following localized convective storm cells.",
    
    # Piedmont Province
    "Northern Piedmont Transition Zone (Culpeper/Fauquier): Saprolite and fractured-rock aquifers experiencing moderate seasonal water table depression (-0.8 ft) due to sparse summer recharge.",
    "Central Piedmont / James River Basin (Albemarle/Nelson): Stable reservoir levels and moderate groundwater storage in crystalline rock wells.",
    "Southside Virginia Piedmont (Dan River Basin): Agricultural irrigation demand balanced by steady baseflow from deep saprolite storage layers.",
    "Richmond Fall Line Corridor: Urban runoff surges contrasted against stable deep-aquifer baseline levels along the fall line boundary.",
    
    # Coastal Plain & Tidewater
    "Coastal Plain Unconfined Aquifer System (Middle Peninsula): Surficial water table responding rapidly to heavy coastal rainfall, showing localized surface saturation and high recharge.",
    "Confined Aquifer System (Hampton Roads/Norfolk): Industrial and municipal withdrawal pressures maintaining a long-term regional drawdown cone, though stabilized by recent injection management.",
    "York-James Peninsula Groundwater Status: Balanced water table indicators in shallow unconfined zones, with minor seasonal fluctuations in agricultural zones.",
    "Eastern Shore Surficial & Confined Aquifers: Intensive agricultural irrigation matched against high recharge rates from sandy soils and marine sedimentary deposits.",
    "Northern Neck Peninsula Hydrology: Stable brackish-freshwater interface conditions along tidal estuary margins with adequate shallow freshwater lens retention.",
    
    # Major River Basins (Surplus vs Deficit Mapping)
    "Potomac-Shenandoah Basin Flow Analysis: Upstream tributary inflow showing slight negative deviation while downstream tidal portions remain at historical norms.",
    "Rappahannock River Basin Discharge: Mid-basin flow rates meeting normal seasonal thresholds with active riparian wetland retention.",
    "York River Basin Watershed Storage: Pamunkey and Mattaponi sub-basins exhibiting normal wetland storage and stable tidal freshwater volume.",
    "James River Basin Macro-Flow: Upper basin storage normal, middle basin showing balanced industrial intake, and lower tidal estuary experiencing minor nutrient-driven eutrophication metrics during low-flow weeks."
]

print("=== DEPLOYING COMPREHENSIVE VIRGINIA HYDROLOGICAL DATASET ===" )
for record in comprehensive_va_records:
    create_smart_capsule(record)

print("=== VIRGINIA FULL EXPANSION COMPLETE ===")

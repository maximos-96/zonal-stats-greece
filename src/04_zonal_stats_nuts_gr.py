from pathlib import Path
import geopandas as gpd
import pandas as pd
from rasterstats import zonal_stats

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data_raw"
DATA_PROCESSED = PROJECT_ROOT / "data_processed"
OUTPUTS = PROJECT_ROOT / "outputs"

nuts_path = DATA_RAW / "NUTS_RG_20M_2024_3035.gpkg"
dem_path = DATA_PROCESSED / "DEM_Greece_30m_3035_clipped.tif"

out_csv = OUTPUTS / "elevation_stats_nuts_gr.csv"
out_gpkg = OUTPUTS / "elevation_stats_nuts_gr.gpkg"
out_layer = "elevation_stats"

OUTPUTS.mkdir(exist_ok=True)

# -----------------------------
# Load NUTS and filter Greece
# -----------------------------
nuts = gpd.read_file(nuts_path)

required_cols = ["CNTR_CODE", "NUTS_ID"]
missing = [c for c in required_cols if c not in nuts.columns]
if missing:
    raise ValueError(f"Missing required columns in NUTS file: {missing}")

nuts_gr = nuts[nuts["CNTR_CODE"] == "EL"].copy()
if nuts_gr.empty:
    raise ValueError("No Greece features found (CNTR_CODE == 'EL').")

# Ensure EPSG:3035 (matches DEM)
nuts_gr = nuts_gr.to_crs("EPSG:3035")

# -----------------------------
# Zonal statistics
# -----------------------------
stats_list = zonal_stats(
    vectors=nuts_gr,
    raster=str(dem_path),
    stats=["mean", "min", "max", "std"],
    nodata=None,         # rasterstats will use raster's nodata if present
    all_touched=False,   # conservative: counts cells whose center is in polygon
    geojson_out=True
)

gdf_stats = gpd.GeoDataFrame.from_features(stats_list, crs=nuts_gr.crs)

# Optional: keep only useful columns + geometry
# (Your NUTS file may include many fields; keep the ones you want for portfolio)
keep_cols = [c for c in ["CNTR_CODE", "NUTS_ID", "LEVL_CODE", "NAME_LATN", "mean", "min", "max", "std", "geometry"]
             if c in gdf_stats.columns]
gdf_stats = gdf_stats[keep_cols].copy()

# -----------------------------
# Exports
# -----------------------------
# CSV (no geometry)
gdf_stats.drop(columns="geometry").to_csv(out_csv, index=False)

# GeoPackage (with geometry)
gdf_stats.to_file(out_gpkg, layer=out_layer, driver="GPKG")

print("Zonal stats complete ✅")
print("CSV:", out_csv)
print("GPKG:", out_gpkg, f"(layer: {out_layer})")
print("Rows:", len(gdf_stats))
print("Example columns:", list(gdf_stats.columns))

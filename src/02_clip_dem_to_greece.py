from pathlib import Path
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import mapping

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data_raw"
DATA_PROCESSED = PROJECT_ROOT / "data_processed"

nuts_path = DATA_RAW / "NUTS_RG_20M_2024_3035.gpkg"
dem_in = DATA_PROCESSED / "DEM_Greece_30m_3035.tif"
dem_out = DATA_PROCESSED / "DEM_Greece_30m_3035_clipped.tif"

# -----------------------------
# Load NUTS (EPSG:3035) and filter Greece
# -----------------------------
nuts = gpd.read_file(nuts_path)

if "CNTR_CODE" not in nuts.columns:
    raise ValueError("Expected column 'CNTR_CODE' not found in NUTS dataset.")

nuts_gr = nuts[nuts["CNTR_CODE"] == "EL"].copy()
if nuts_gr.empty:
    raise ValueError("No features found for Greece (CNTR_CODE == 'EL').")

# Ensure correct CRS
nuts_gr = nuts_gr.to_crs("EPSG:3035")

# Dissolve to one geometry (whole Greece)
greece_geom = nuts_gr.geometry.union_all()

# -----------------------------
# Clip raster
# -----------------------------
with rasterio.open(dem_in) as src:
    # If DEM CRS differs, stop early (we can reproject if needed)
    if src.crs is None:
        raise ValueError("Input DEM has no CRS defined.")
    if src.crs.to_string() != "EPSG:3035":
        raise ValueError(f"DEM CRS is {src.crs}, expected EPSG:3035. Reproject step needed.")

    out_image, out_transform = mask(
        src,
        [mapping(greece_geom)],
        crop=True,
        nodata=src.nodata
    )

    out_meta = src.meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

DATA_PROCESSED.mkdir(exist_ok=True)

with rasterio.open(dem_out, "w", **out_meta) as dst:
    dst.write(out_image)

print("Clipped DEM created:")
print(dem_out)

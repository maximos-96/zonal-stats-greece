from pathlib import Path
import rasterio
from rasterio.merge import merge

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data_raw"
DATA_PROCESSED = PROJECT_ROOT / "data_processed"

dem_files = [
    DATA_RAW / "DEM_Raw_30_pt1.tif",
    DATA_RAW / "DEM_Raw_30_pt2.tif",
]
output_dem = DATA_PROCESSED / "DEM_Greece_30m.tif"

DATA_PROCESSED.mkdir(exist_ok=True)

srcs = [rasterio.open(fp) for fp in dem_files]
mosaic, out_transform = merge(srcs)

out_meta = srcs[0].meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_transform
})

with rasterio.open(output_dem, "w", **out_meta) as dst:
    dst.write(mosaic)

for src in srcs:
    src.close()

print("DEM mosaic created:", output_dem)

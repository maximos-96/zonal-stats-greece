from pathlib import Path
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = PROJECT_ROOT / "data_processed"

dem_in = DATA_PROCESSED / "DEM_Greece_30m.tif"
dem_out = DATA_PROCESSED / "DEM_Greece_30m_3035.tif"

dst_crs = "EPSG:3035"

with rasterio.open(dem_in) as src:
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds
    )

    meta = src.meta.copy()
    meta.update({"crs": dst_crs, "transform": transform, "width": width, "height": height})

    with rasterio.open(dem_out, "w", **meta) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.bilinear
            )

print("Reprojected DEM created:", dem_out)

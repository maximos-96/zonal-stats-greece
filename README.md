## Project Structure
```text
zonal_stats_greece/
├─ data_raw/               # Raw input data
├─ data_processed/         # Intermediate rasters
├─ outputs/                # Final outputs (CSV, GPKG, PNG)
├─ src/                    # Python scripts
│  ├─ 01_mosaic_dem.py
│  ├─ 02_clip_dem_to_greece.py
│  ├─ 03_reproject_dem_to_3035.py
│  ├─ 04_zonal_stats_nuts_gr.py
│  └─ 05_map_mean_elevation.py
├─ environment.yml
├─ SETUP.md
└─ README.md
```

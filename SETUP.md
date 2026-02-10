# Environment Setup (Windows)

This project uses a Conda environment via Miniforge to ensure
stable installation of GIS libraries (GDAL, Rasterio, GeoPandas).

## Requirements
- Windows 10 / 11
- Miniforge3 (x86_64)
- VS Code (with Python extension)

## Create environment
Open Miniforge Prompt and run:

```bash
conda create -n zonalstats python=3.11
conda activate zonalstats
conda install -c conda-forge geopandas rasterio rasterstats matplotlib pandas numpy

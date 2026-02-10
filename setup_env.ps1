# ---------------------------------------
# GIS Python environment setup (Windows)
# ---------------------------------------

# Create conda environment
conda create -n zonalstats python=3.11 -y

# Activate environment
conda activate zonalstats

# Install GIS stack from conda-forge
conda install -c conda-forge `
    geopandas `
    rasterio `
    rasterstats `
    matplotlib `
    pandas `
    numpy `
    -y

# Test imports
python - << EOF
import geopandas
import rasterio
from rasterstats import zonal_stats
print("GIS environment setup OK")
EOF

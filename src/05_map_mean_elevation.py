from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = PROJECT_ROOT / "outputs"

gpkg_path = OUTPUTS / "elevation_stats_nuts_gr.gpkg"
layer_name = "elevation_stats"

out_png = OUTPUTS / "mean_elevation_nuts_gr.png"

# -----------------------------
# Load data
# -----------------------------
gdf = gpd.read_file(gpkg_path, layer=layer_name)

if "mean" not in gdf.columns:
    raise ValueError("Column 'mean' not found in zonal stats output.")

# -----------------------------
# Plot
# -----------------------------
fig, ax = plt.subplots(1, 1, figsize=(10, 12))

gdf.plot(
    column="mean",
    ax=ax,
    cmap="terrain",
    legend=True,
    legend_kwds={
        "label": "Mean elevation (m)",
        "shrink": 0.6
    },
    edgecolor="black",
    linewidth=0.3
)

ax.set_title(
    "Mean Elevation per NUTS Region in Greece\n(Copernicus DEM 30 m)",
    fontsize=14
)

ax.axis("off")

plt.tight_layout()
plt.savefig(out_png, dpi=300)
plt.close()

print("Map exported:")
print(out_png)

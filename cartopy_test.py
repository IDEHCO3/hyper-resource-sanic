import cartopy
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from shapely.geometry import shape
import cartopy.crs as ccrs
import requests
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(), frameon=False)
ax.set_extent([-74.018, -28.877, -33.742, 5.2672], ccrs.PlateCarree())
ax.patch.set_visible(False)
res = requests.get('http://127.0.0.1:8000/lim-unidade-federacao-a-list')
data = res.json()
features = data['features']
geometries = [shape(f['geometry']) for f in features]
ax.add_geometries(geometries, ccrs.PlateCarree(), facecolor='#C8A2C8', alpha=0.5, edgecolor="black")
#ax = plt.axes(projection=cartopy.crs.PlateCarree())
#ax.add_feature(geometries, linewidth=.5, edgecolor="black")
# %% 0. Libraries
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely import wkt
from source import utils as ut

# %% 1. General settings
option_settings = {
    'display.max_rows': False,
    'display.max_columns': None,
    'display.float_format': '{:,.10f}'.format
}
[pd.set_option(option, setting) for option, setting in option_settings.items()]

gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

IN_PATH = 'data/in/'
OUT_PATH = 'data/out/'
CITY = 'Arequipa'
THRESHOLD = 3.5

# %% 2. Load data
filename = 'Arequipa.kml'
gdf_aqp = gpd.read_file(IN_PATH + filename, driver='KML')

filename = 'partners_location.csv'
df_prt = pd.read_csv(IN_PATH + filename)

# %% 3. Format data
gdf_aqp.drop(columns='Description', inplace=True)
gdf_aqp.columns = map(str.lower, gdf_aqp.columns)

df_prt = df_prt[df_prt['city'] == CITY]
gdf_prt = gpd.GeoDataFrame(
    df_prt,
    geometry=gpd.points_from_xy(df_prt.longitude, df_prt.latitude)
)

# %% 4. Algorithm 
results = ut.nearest_supply(gdf_prt, gdf_aqp, 'vendor_id', THRESHOLD)

# %% 5. Vertical outputs
verticals = gdf_prt.vertical.unique()
vert_results = {}
for i, v in enumerate(verticals):
    print(v)
    vert_results[v] = ut.nearest_supply(gdf_prt[gdf_prt.vertical == v], gdf_aqp, 'vendor_id', THRESHOLD)
    print('---------------------------------------')

# %% 5. Export
filename = 'arequipa_results.xlsx'
results.to_excel(OUT_PATH + filename)


# %% 0. Libraries
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely import wkt

# %% 1. General settings
option_settings = {
    'display.max_rows': None,
    'display.max_columns': False,
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

filename = 'partner_location.csv'
df_prt = pd.read_csv(IN_PATH + filename)

# %% 3. Format data
gdf_aqp.drop(columns='Description', inplace=True)
gdf_aqp.columns = map(str.lower, gdf_aqp.columns)

df_prt = df_prt[df_prt['city'] == CITY]
gdf_prt = gpd.GeoDataFrame(
    df_prt,
    geometry=gpd.points_from_xy(df_prt.longitude, df_prt.latitude)
)

# %% 3. Algorithm
total_stores = len(gdf_prt.vendor_id.unique())

for i, r in gdf_aqp.iterrows():
    exp_zone = r[0]
    zone_centroid = r[1].centroid

    gdf_prt[f'dist_to_{exp_zone}'] = gdf_prt['geometry'].distance(zone_centroid)*100 # in KM
    mask = gdf_prt[f'dist_to_{exp_zone}'] <= THRESHOLD
    gdf_prt.loc[mask, f'near_to_{exp_zone}'] = 1
    gdf_prt[f'near_to_{exp_zone}'].fillna(0, inplace=True) 

    qty_stores = gdf_prt[f'near_to_{exp_zone}'].sum()
    print(f'There are {qty_stores} stores ({round(qty_stores/total_stores*100, 2)}%) near to "{exp_zone}"')

# TODO: Plot

# %% 4. Export
filename = 'AQP_exp.csv'
gdf_prt.to_csv(OUT_PATH + filename, sep=';')

# %%

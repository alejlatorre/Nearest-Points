# %% 0. Libraries
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely import wkt

# %% 1. General settings
option_settings = {
    'display.max_rows': None,
    'display.max_columns': False,
    'display.float_format': '{:,.2f}'.format
}
[pd.set_option(option, setting) for option, setting in option_settings.items()]

gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

IN_PATH = 'data/in/'
OUT_PATH = 'data/out/'

# %% 2. Load data
filename = 'Arequipa.kml'
gdf_aqp = gpd.read_file(IN_PATH + filename, driver='KML')
gdf_aqp.drop(columns='Description', inplace=True)
gdf_aqp.columns = map(str.lower, df.columns)

filename = 'partner_location.csv'
df_prt = pd.read_csv(IN_PATH + filename)
gdf_prt = geopandas.GeoDataFrame(
    df_prt, 
    geometry=geopandas.points_from_xy(df_prt.longitude, df_prt.latitude)
)

# %% 

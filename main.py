# %%
import numpy as np
import pandas as pd
import geopandas as gpd

# %% 
option_settings = {
    'display.max_rows': None,
    'display.max_columns': False,
    'display.float_format': '{:,.2f}'.format
}
[pd.set_option(option, setting) for option, setting in option_settings.items()]

gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

IN_PATH = 'data/in/'
OUT_PATH = 'data/out/'

# %%
filename = 'Arequipa.kml'
df = gpd.read_file(IN_PATH + filename, driver='KML')

df.drop(columns='Description', inplace=True)
df.columns = map(str.lower, df.columns)

# %%

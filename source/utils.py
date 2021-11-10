import geopandas as gpd
from shapely import wkt

def nearest_supply(gdf, polygons, ids, threshold):
    gdf_ = gdf.copy()
    total_stores = len(gdf_[ids].unique())

    for i, r in polygons.iterrows():
        expansion_zone = r[0]
        zone_centroid = r[1].centroid

        gdf_[f'dist_to_{expansion_zone}'] = gdf_['geometry'].distance(zone_centroid)*100 # in KM
        mask = gdf_[f'dist_to_{expansion_zone}'] <= threshold
        gdf_.loc[mask, f'near_to_{expansion_zone}'] = 1
        gdf_[f'near_to_{expansion_zone}'].fillna(0, inplace=True) 

        nearest_stores = gdf_[f'near_to_{expansion_zone}'].sum()
        print(f'There are {nearest_stores} stores ({round(nearest_stores/total_stores*100, 2)}%) near to "{expansion_zone}"')

    return gdf_

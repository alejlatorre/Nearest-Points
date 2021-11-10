import geopandas as gpd
from shapely import wkt

def nearest_supply(gdf, polygons, ids, threshold):
    """
    Compute distance between each stores and zones centroid.
    Also, identifies if this distance is less than threshold.
    Parameters
    ----------
    gdf : dataframe of shape (n_stores, n_features)
        Data of each store.
    polygons : dataframe of shape (n_zones, 2)
        Data of proposed zone polygons.
    ids : list
        List of store IDs.
    threshold : int
        Limit distance that is required in evaluation.
    Returns
    -------
    gdf_ : dataframe
        Data of each store with distance between its coordinates and centroid of each proposed zone. 
        Also, it has an identifier that is 1 if computed distance is less than threshold and 0 if it is greather.
    """

    gdf_ = gdf.copy()
    total_stores = len(gdf_[ids].unique())

    print(f'Total: {total_stores}')
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
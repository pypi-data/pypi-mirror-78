import requests
import re
import pandas as pd
import geopandas as gpd

def geocode(address):
    coords = {}

    address = list(address)

    address = [item.replace(', Grand Rapids, MI', '')
               .replace('/', '%26')
               for item in address]

    address = [re.sub(r'\(.*\)', '', item) for item in address]
    address = [re.sub(r'\s+', ' ', item) for item in address]

    for item in address:
        latlon = requests.get(str(
            'https://maps.grcity.us/arcgis/rest/services/Geocode/Transport_StreetCenterlines/GeocodeServer/findAddressCandidates?Street=' + \
            item.upper() + \
            '&outSR=4326&f=pjson'))
        latlon = latlon.json()
        if 'candidates' in latlon and len(latlon['candidates']) > 0:
            coords[item] = str(latlon['candidates'][0]['location']['x']) + ',' + str(latlon['candidates'][0]['location']['y'])

    return coords

def label_points_polygon(polygons, points, label):
    # Label 311 Data with ACS Boundary IDs
    labels = {}

    for index, point in points.iterrows():
        for number, polygon in polygons.iterrows():
            if pd.notna(polygon['geometry']) and pd.notna(point['geometry']):
                if polygon['geometry'].contains(point['geometry']):
                    labels[index] = polygon[label]

    return(labels)

import requests
import pandas as pd
import io


def elevation(lat=(40, 41), lon=(-65, -60)):
    """
    Function to request data from SRTM30.
    Bathymetry / Topography (SRTM30) is a global bathymetry/topography data product distributed by the USGS EROS data
    center. The data product has a resolution of 30 seconds (roughly 1 km).
    :param lat: tuple with min and max latitude
    :param lon: tuple with min and max longitude
    :return: dataframe
    """

    class ElevationSurface(object):
        def __init__(self):

            # Definine the domain of interest
            minlat = lat[0]
            maxlat = lat[1]
            minlon = lon[0]
            maxlon = lon[1]

            url = 'http://coastwatch.pfeg.noaa.gov/erddap/griddap/usgsCeSrtm30v6.csv?topo[(' + str(maxlat) + '):1:(' + \
                  str(minlat) + ')][(' + str(minlon) + '):1:(' + str(maxlon) + ')]'
            s = requests.get(url).content
            df = pd.read_csv(io.StringIO(s.decode('utf-8')), header=0)
            df.reset_index(drop=True)
            df.drop(0, inplace=True)
            df = df[['latitude', 'longitude', 'topo']].astype(float)
            df.rename(columns={'latitude': 'lat', 'longitude': 'lon', 'topo': 'elev'}, inplace=True)

            self.data = df

        def plot(self):

            import plotly.graph_objects as go
            from numpy import array, unique

            lon = unique(self.data.lon)
            lat = unique(self.data.lat)

            elev = array([self.data.elev[i: i + len(lon)] for i in range(0, len(self.data.elev), len(lon))])

            fig = go.Figure(data=[go.Surface(z=elev, x=lon, y=lat)])
            fig.update_layout(scene=dict(
                xaxis_title='Lon, °',
                yaxis_title='Lat, °',
                zaxis_title='Elevation, m'))
            fig.show()

    return ElevationSurface()


def point_elev(lat, lon):
    minlat = lat - 0.001
    maxlat = lat + 0.001
    minlon = lon - 0.001
    maxlon = lon + 0.001
    c = elevation(lat=(minlat, maxlat), lon=(minlon, maxlon))
    znew = round(c.data.elev.mean())

    return znew


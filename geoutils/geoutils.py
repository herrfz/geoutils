"""
Utilities for geographical calculations
http://www.movable-type.co.uk/scripts/latlong.html
Eriza Fazli, 2015
"""
from math import radians, degrees, sqrt, pow, sin, asin, cos, atan2

R = 6371


class Point(object):
    def __init__(self, lat, lon):
        """in degrees"""
        self._lat = lat
        self._lon = lon

    @classmethod
    def from_radians(cls, lat, lon):
        return cls(degrees(lat), degrees(lon))

    @property
    def lat(self):
        return radians(self._lat)

    @lat.setter
    def lat(self, lat):
        self._lat = lat

    @property
    def lon(self):
        return radians(self._lon)

    @lon.setter
    def lon(self, lon):
        self._lon = lon

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point.from_radians(self.lat - other.lat, self.lon - other.lon)
        else:
            return NotImplemented


def haversine_distance(*points):
    """
    points is (Point1, Point2)
    """
    start, end = points
    delta = end - start
    a = pow(sin(delta.lat / 2), 2) +\
        cos(start.lat)*cos(end.lat)*pow(sin(delta.lon / 2), 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def bearing(*points):
    """
    points is (Point1, Point2)
    """
    start, end = points
    delta = end - start
    theta = atan2(sin(delta.lon)*cos(end.lat),
       cos(start.lat)*sin(end.lat) - sin(start.lat)*cos(end.lat)*cos(delta.lon))
    return degrees(theta)


def endpoint(start, bearing, distance):
    """
    start is Point
    bearing is in degree
    distance is in km
    """
    delta = distance / R
    bearing = radians(bearing)
    end_lat = asin(sin(start.lat)*cos(delta) + cos(start.lat)*sin(delta)*cos(bearing))
    end_lon = start.lon + atan2(sin(bearing)*sin(delta)*cos(start.lat),
        cos(delta) - sin(start.lat)*sin(end_lat))
    return Point.from_radians(end_lat, end_lon)


def great_circle_route(start, end, resolution):
    """
    start, end are Point
    resolution is in km
    """
    final = end
    points = []
    points.append(start)
    distance = haversine_distance(start, end)
    n_segments = int(distance / resolution) - 1
    direction = bearing(start, end)
    for i in range(n_segments):
        end = endpoint(start, direction, resolution)
        direction = (bearing(end, start) + 180) % 360
        points.append(end)
        start = end
    points.append(final)
    return points


def from_dms(degree, minute, second, direction):
    """
    degree, minute, second are positive integers
    direction is in ['N', 'S', 'E', 'W']
    """
    sign = -1 if direction in ['S', 'W'] else 1
    return sign * (degree + minute/60 + second/3600)


def to_dms(degree, to_dir):
    """
    degrees is float
    to_dir is in ['lat', 'lon']
    """
    if to_dir == 'lat':
        suffix = 'N' if degree >= 0 else 'S'
    elif to_dir == 'lon':
        suffix = 'E' if degree >= 0 else 'W'
    else:
        raise ValueError
    degs = int(abs(degree))
    mins = int((abs(degree) - degs) * 60)
    secs = int((abs(degree) - degs - mins/60) * 3600)
    return degs, mins, secs, suffix

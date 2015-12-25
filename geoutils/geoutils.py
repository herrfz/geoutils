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
        self.lat = lat
        self.lon = lon

    def to_radians(self):
        self.lat = radians(self.lat)
        self.lon = radians(self.lon)

    def to_degrees(self):
        self.lat = degrees(self.lat)
        self.lon = degrees(self.lon)


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


def haversine_distance(*points):
    """
    points is (Point1, Point2)
    """
    start = Point(points[0].lat, points[0].lon)
    end = Point(points[1].lat, points[1].lon)
    start.to_radians()
    end.to_radians()
    delta_lat = end.lat - start.lat
    delta_lon = end.lon - start.lon
    a = pow(sin(delta_lat / 2), 2) +\
        cos(start.lat)*cos(end.lat)*pow(sin(delta_lon / 2), 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def bearing(*points):
    """
    points is (Point1, Point2)
    """
    start = Point(points[0].lat, points[0].lon)
    end = Point(points[1].lat, points[1].lon)
    start.to_radians()
    end.to_radians()
    delta_lon = end.lon - start.lon
    theta = atan2(sin(delta_lon)*cos(end.lat),
       cos(start.lat)*sin(end.lat) - sin(start.lat)*cos(end.lat)*cos(delta_lon))
    return degrees(theta)


def endpoint(start, bearing, distance):
    """
    start is Point
    bearing is in degree
    distance is in km
    """
    start = Point(start.lat, start.lon)
    start.to_radians()
    delta = distance / R
    bearing = radians(bearing)
    end_lat = asin(sin(start.lat)*cos(delta) + cos(start.lat)*sin(delta)*cos(bearing))
    end_lon = start.lon + atan2(sin(bearing)*sin(delta)*cos(start.lat),
        cos(delta) - sin(start.lat)*sin(end_lat))
    end = Point(end_lat, end_lon)
    end.to_degrees()
    return end


def great_circle_route(start, end, resolution):
    """
    start, end are Point
    resolution is in km
    """
    points = []
    points.append(start)
    final = Point(end.lat, end.lon)
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

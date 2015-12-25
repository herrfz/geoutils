from nose.tools import *
from geoutils import *

point1 = Point(from_dms(50, 3, 59, 'N'), from_dms(5, 42, 53, 'W'))
point2 = Point(from_dms(58, 38, 38, 'N'), from_dms(3, 4, 12, 'W'))
point3 = Point(from_dms(53, 19, 14, 'N'), from_dms(1, 43, 47, 'W'))

ref_lats = [50.06638888888889,
            50.95412545484834,
            51.84140782540385,
            52.72820278406647,
            53.6144739215198,
            54.5001812413642,
            55.385280706547405,
            56.26972371588522,
            57.15345649787652,
            58.64388888888889]

ref_lons = [-5.714722222222222,
            -5.488452925623853,
            -5.253372447101052,
            -5.008841420702164,
            -4.754159689826889,
            -4.488558902871845,
            -4.211194014076846,
            -3.9211334981677983,
            -3.6173480487160177,
            -3.0700000000000003]


def test_point():
    a = Point(48, 11)
    b = Point.from_radians(radians(48), radians(11))
    assert_almost_equal(a.lat, radians(48))
    assert_almost_equal(a.lon, radians(11))
    assert_almost_equal(b.lat, radians(48))
    assert_almost_equal(b.lon, radians(11))


def test_from_dms():
    assert_almost_equal(from_dms(50, 3, 59, 'N'), 50.06638888888889)
    assert_almost_equal(from_dms(5, 42, 53, 'W'), -5.714722222222222)


def test_to_dms():
    assert_equal(to_dms(50.06638888888889, 'lat'), (50, 3, 58, 'N'))
    assert_equal(to_dms(-5.714722222222222, 'lon'), (5, 42, 52, 'W'))
    assert_equal(to_dms(9.119818104504075, 'lat'), (9, 7, 11, 'N'))
    assert_equal(to_dms(11.275201271425743, 'lat'), (11, 16, 30, 'N'))


def test_haversine_distance():
    assert_almost_equal(haversine_distance(point1, point2), 968.8535467131387)


def test_bearing():
    assert_almost_equal(bearing(point1, point2), 9.119818104504075)
    assert_almost_equal((bearing(point2, point1) + 180) % 360, 11.275201271425743)


def test_endpoint():
    end = endpoint(point3, from_dms(96, 1, 18, 'N'), 124.8)
    assert_equal(to_dms(end._lat, 'lat'), (53, 11, 17, 'N'))
    assert_equal(to_dms(end._lon, 'lon'), (0, 7, 59, 'E'))


def test_great_circle_route():
    points = great_circle_route(point1, point2, 100)
    lats = (x._lat for x in points)
    lons = (x._lon for x in points)
    dlats = sum((x - y for x in lats for y in ref_lats))
    dlons = sum((x - y for x in lons for y in ref_lons))
    assert_almost_equal(dlats, 0)
    assert_almost_equal(dlons, 0)

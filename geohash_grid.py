import geohash
from shapely import geometry, Polygon
import json
def is_geohash_in_bounding_box(current_geohash, bbox_coordinates):
    coordinates = geohash.decode(current_geohash)
    geohash_in_bounding_box = (bbox_coordinates[0] < coordinates[0] < bbox_coordinates[2]) and (
            bbox_coordinates[1] < coordinates[1] < bbox_coordinates[3])
    return geohash_in_bounding_box

def build_geohash_box(current_geohash):
    b = geohash.bbox(current_geohash)
    polygon = [(b['w'], b['s']), (b['w'], b['n']), (b['e'], b['n']), (b['e'], b['s'],), (b['w'], b['s'])]
    return polygon

def compute_geohash_tiles(bbox_coordinates):
    checked_geohashes = set()
    geohash_stack = set()
    geohashes = []
    center_latitude = (bbox_coordinates[0] + bbox_coordinates[2]) / 2
    center_longitude = (bbox_coordinates[1] + bbox_coordinates[3]) / 2

    center_geohash = geohash.encode(center_latitude, center_longitude, precision=7)
    geohashes.append(center_geohash)
    geohash_stack.add(center_geohash)
    checked_geohashes.add(center_geohash)
    while len(geohash_stack) > 0:
        current_geohash = geohash_stack.pop()
        neighbors = geohash.neighbors(current_geohash)
        for neighbor in neighbors:
            if neighbor not in checked_geohashes and is_geohash_in_bounding_box(neighbor, bbox_coordinates):
                geohashes.append(neighbor)
                geohash_stack.add(neighbor)
                checked_geohashes.add(neighbor)
    return geohashes



def compute_geohash_tiles_from_polygon(polygon):
    checked_geohashes = set()
    geohash_stack = set()
    geohashes = []
    center_latitude = polygon.centroid.coords[0][1]
    center_longitude = polygon.centroid.coords[0][0]

    center_geohash = geohash.encode(center_latitude, center_longitude, precision=7)
    geohashes.append(center_geohash)
    geohash_stack.add(center_geohash)
    checked_geohashes.add(center_geohash)
    while len(geohash_stack) > 0:
        current_geohash = geohash_stack.pop()
        neighbors = geohash.neighbors(current_geohash)
        for neighbor in neighbors:
            point = geometry.Point(geohash.decode(neighbor)[::-1])
            if neighbor not in checked_geohashes and polygon.contains(point):
                geohashes.append(neighbor)
                geohash_stack.add(neighbor)
                checked_geohashes.add(neighbor)
    return geohashes

polygon = Polygon(json.load(open('geohash/taipei_polygon1.geojson', 'r'))['features'][0]['geometry']['coordinates'][0][0])
# print(polygon)
# geohashes_list = compute_geohash_tiles([24.90631745644159, 121.3567187208344, 25.198716653865162, 121.71560516498928])
geohashes_list = compute_geohash_tiles_from_polygon(polygon)
import geojson
from geojson import MultiLineString

def write_geohash_layer(geohashes):
    """Writes a grid layer based on the geohashes

    :param geohashes: a list of geohashes
    """

    layer = MultiLineString([build_geohash_box(gh) for gh in geohashes])
    json = {
        "type": "FeatureCollection",
        "features": [
            {
            "type": "Feature",
            "geometry": {
                "type": "Polygon", 
                "coordinates": layer['coordinates']}
            }
        ]
    }
    with open('world_geohash_grids.json', 'wb') as f:
        f.write(geojson.dumps(json).encode('utf-8'))

write_geohash_layer(geohashes_list)
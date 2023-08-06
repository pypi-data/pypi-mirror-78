from geoformat_lib.geoprocessing.measure.distance import (
    euclidean_distance,
    manhattan_distance
)
from geoformat_lib.conversion.geometry_conversion import (
    geometry_to_geometry_collection,
    multi_geometry_to_single_geometry
)
from geoformat_lib.geoprocessing.connectors.operations import (
    coordinates_to_segment
)


def segment_length(segment, distance_type='EUCLIDEAN'):
    """
    Calculate length of a given segment
    """
    (point_a, point_b) = segment
    if distance_type.upper() == 'EUCLIDEAN':
        return euclidean_distance(point_a, point_b)
    elif distance_type.upper() == 'MANHATTAN':
        return manhattan_distance(point_a, point_b)
    else:
        print('type of distance : {distance_type} does not exists'.format(distance_type=distance_type))


def geometry_length(geometry, distance_type='EUCLIDEAN'):


    # initialize return
    length = 0

    # transform function to geometry collection
    geometry = geometry_to_geometry_collection(geometry)
    # if geometry is not empty
    if geometry:
        for geometry in geometry['geometries']:
            # if geometry is not a point or multipoint (they are no dimension then no length)
            if 'POINT' not in geometry['type'].upper():
                # loop over part
                for geometry_part in multi_geometry_to_single_geometry(geometry, bbox=False):
                    coordinates_list = geometry_part['coordinates']
                    # if there is coordinates
                    if coordinates_list:
                        # transform coordinates_list to segment and calculate segment lenght
                        for segment in coordinates_to_segment(coordinates_list):
                            # add distance to
                            length += segment_length(segment, distance_type=distance_type)

        return length
def coordinates_to_point(coordinates):
    """
    With geometry coordinates this function return each point individually in iterator
    :param coordinates
    :yield point coordinate
    """

    if isinstance(coordinates[0], (int, float)):
        yield coordinates
    else:
        for inner_coordinates in coordinates:
            for point in coordinates_to_point(inner_coordinates):
                yield point


def coordinates_to_segment(coordinates):
    """
    This function yield
    :param coordinates:
    :return:
    """
    if isinstance(coordinates[0][0], (float, int)):
        for i, point in enumerate(coordinates_to_point(coordinates)):
            if i == 0:
                pass
            else:
                yield [save_point, point]
            save_point = point
    else:
        for part_coordinates in coordinates:
            for segment in coordinates_to_segment(part_coordinates):
                yield segment


def coordinates_to_bbox(coordinates):
    """
    This function return boundaries box (bbox) from geometry coordinates.
    It's works with 2 to n-dimensional data.
    (x_min, y_min, n_min, x_max, y_max, n_max)

    """
    # if list is not empty
    if coordinates:
        # loop on each coordinates
        for i_pt, point in enumerate(coordinates_to_point(coordinates)):
            # create empty bbox at first iteration
            if i_pt == 0:
                bbox = [None] * (len(point) * 2)
            # loop on dimension of coordinate
            for i_coord, pt_coord in enumerate(point):
                # add data at first iteration
                if i_pt == 0:
                    bbox[i_coord] = pt_coord

                test_value_min_tuple = (bbox[i_coord], pt_coord)
                bbox[i_coord] = min(value for value in test_value_min_tuple if value is not None)
                test_value_max_tuple = (bbox[i_coord + len(point)], pt_coord)
                bbox[i_coord + len(point)] = max(value for value in test_value_max_tuple if value is not None)

        return tuple(bbox)
    else:
        return ()


def segment_to_bbox(segment):
    """
    Return bbox to given segment

    :param segment: segment of which we want to know the bbox
    :return: bbox of segment
    """
    x, y = zip(*segment)

    return min(x), min(y), max(x), max(y)

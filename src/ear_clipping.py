import numpy as np


def ear_clipping(vertices: np.ndarray, path: np.ndarray):
    """
    A fast way to triangulate a polygon

    :param vertices: coordinated of all points
    :param path: indices of the vertices by which form a polygone
    :return:
    """

    if is_self_intersecting(vertices, path):
        raise Exception("Ear-Clipping doesn't work with self intersection polygons")

    # make sure that the direction is contre-clockwise
    path = orient_path(vertices, path)

    # polygon should contain at least 3 points,
    if len(np.unique(path)) < 3:
        raise Exception("Polygon has too few vertices on the path")

    # # get vertices by the path
    # vertices = vertices[path]

    triangles = []
    # rest = list(path[:-1])
    rest = list(path)

    while len(rest) > 3:
        rest_len = len(rest)
        for i in range(rest_len):
            id0 = rest[(i - 1) % rest_len]
            id1 = rest[i]
            id2 = rest[(i + 1) % rest_len]

            p0 = vertices[id0]
            p1 = vertices[id1]
            p2 = vertices[id2]

            if not is_convex(p0, p1, p2):
                continue

            is_ear = True
            for j in rest:
                if not ([id0, id1, id2] == j).any() and is_point_in_triangle(vertices[j], p0, p1, p2):
                    is_ear = False
                    break

            if is_ear:
                triangles.append([id0, id1, id2])
                del rest[i]
                break

    triangles.append(rest)

    return triangles


def is_point_in_triangle(p, a, b, c):
    abc = np.linalg.norm(np.cross(b - a, c - a))
    u = np.linalg.norm(np.cross(p - b, c - b)) / abc
    v = np.linalg.norm(np.cross(p - c, a - c)) / abc
    w = np.linalg.norm(np.cross(p - a, b - a)) / abc

    return np.isclose(u + v + w, 1)


def is_convex(p0, p1, p2):
    """
    Points should be in contr-clockwise order

    :param p0:
    :param p1:
    :param p2:
    :return:
    """
    normal = np.cross(p2 - p1, p0 - p1)

    if len(p0) == 2:
        return normal > 0
    else:
        return normal[2] > 0


def orient_path(vertices: np.ndarray, path: np.ndarray):
    """
    Checks if the path is clockwise or counter-clockwise
    In case if the path is clockwise, the path will be flipped

    :param vertices:
    :param path:
    :return:
    """

    if path[0] != path[-1]:
        path = np.append(path, path[0])

    # zipping path to edges
    prev_vertices = vertices[path[:-1]]
    next_vertices = vertices[path[1:]]

    res = np.sum((next_vertices[:, 0] - prev_vertices[:, 0]) * (next_vertices[:, 1] + prev_vertices[:, 1]))

    path = path[:-1]

    return path if res < 0 else np.flip(path)


def is_self_intersecting(vertices: np.ndarray, path: np.ndarray):
    """
    Check if the any edge of the polygon intersects another edge

    TODO implementation is not a part of the current article
    :param vertices:
    :param path:
    :return:
    """
    return False

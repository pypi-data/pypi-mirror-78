from helper import build_dist_matrix, open_file
from routefinder import RouteFinder


def test_distance():
    v3 = "../py2opt/dataset.txt"
    cities_coordinates, cities_names, num_cities = open_file(v3)
    distance_matrix = build_dist_matrix(cities_names, cities_coordinates)
    route_finder = RouteFinder(distance_matrix, cities_names)
    best_distance, best_route, best_distances = route_finder.solve()
    assert best_distance < 90000

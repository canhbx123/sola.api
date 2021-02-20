from math import sin, cos, sqrt, atan2, radians


class DistanceUtil:
    # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    @staticmethod
    def get_distance2coord(coord1, coord2):
        R = 6373.0
        lat1 = radians(coord1[0])
        lon1 = radians(coord1[1])
        lat2 = radians(coord2[0])
        lon2 = radians(coord2[1])
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c


if __name__ == '__main__':
    distance = DistanceUtil.get_distance2coord([21.076545958078665, 105.70070295103913], [21.053349896661516, 105.73511530447112])
    print(distance)

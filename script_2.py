import random
import matplotlib.pyplot as plt


"""
15 * 20 = 300

WIDTH * HEIGHT = AREA

AREA % (NUM_SMALL + NUM_LARGE * 2) = ...

300 / 21 = 14.285714285714286 +- 1

lista do trzymania punktow prostokatow rooms = [(p1,p2), (p3,p4), (p5,p6), (p7,p8)]

AREA - AREA(ROOMS) = jak najmniejsze

Area(ROOMS) = suma powierzchni prostokatow - suma powierzchni przeciec

"""

def rooms_overlap(rooms: list):
    overlap = 0
    for i, room1 in enumerate(rooms):
        for j, room2 in enumerate(rooms):
            if i != j:
                x1, y1 = room1
                x2, y2 = room2

    return overlap


def main(width: int, height: int, small: int, large: int):
    rooms = small + large
    area = width * height

    room_area = area / rooms
    room_area_range = (room_area - 1, room_area + 1)


if __name__ == "__main__":
    pass
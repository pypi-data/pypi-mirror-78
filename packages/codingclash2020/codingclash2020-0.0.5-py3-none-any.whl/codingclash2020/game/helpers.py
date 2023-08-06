import math

def dist(loc1, loc2):
    return (loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2

def squares_within_distance(radius_squared):
    radius = math.ceil(math.sqrt(radius_squared))
    squares = []
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dist((0,0), (dx, dy)) <= radius_squared:
                squares.append((dx, dy))
    return squares

def in_between(pointa, pointb, pointc):
    dx = pointb[0] - pointa[0]
    dy = pointb[1] - pointa[1]

    ranx = sorted([pointa[0], pointb[0]])
    rany = sorted([pointa[1], pointb[1]])

    if not (ranx[0] < pointc[0] < ranx[1] and rany[0] < pointc[1] < rany[1]): return False

    linex = lambda x: pointa[1] + dy / dx * (x - pointa[0])

    if dx == 0:
        r = sorted([pointa[1], pointb[1]])
        if pointc[0] == pointa[0] and r[0] < pointc[1] < r[1]: return True

    elif (linex(pointc[0]) <= pointc[1] and linex(pointc[0]) + 1 > pointc[1]) or (
            linex(pointc[0]) >= pointc[1] and linex(pointc[0]) + 1 < pointc[1]):
        return True

    return False

import random
import math
from queue import Queue

random.seed(1)  # Setting random number generator seed for repeatability

NUM_DRONES = 10000
AIRSPACE_SIZE = 128000 # 128 km
CONFLICT_RADIUS = 500 # Meters.

def collide(drone1, drone2, radius):
    distance = math.sqrt((drone1[0] - drone2[0]) ** 2 + (drone1[1] - drone2[1]) ** 2)

    if(distance < 2 * radius):
        return True

    return False

def count_conflicts(drones, conflict_radius):
    conflicted = 0
    drones = sorted(drones, key=lambda drone: drone[0])
    q = Queue()

    # drop all that don't collide in x
    for drone in drones:
        this_conflicts = False
        [x, _] = drone

        more = not q.empty()
        while more:
            [[top_x, _], _] = q.queue[0]
            if top_x + conflict_radius <= x - conflict_radius:
                q.get()
                more = not q.empty()
            else:
                more = False

        for other in q.queue:
            (other_drone, other_conflicts) = other
            if collide(other_drone, drone, conflict_radius):
                if not other_conflicts:
                    other[1] = True
                    conflicted += 1

                if not this_conflicts:
                    this_conflicts = True
                    conflicted += 1

        q.put([drone, this_conflicts])

    return conflicted

def gen_coord():
    return int(random.random() * AIRSPACE_SIZE)

positions = [[gen_coord(), gen_coord()] for i in range(NUM_DRONES)]
conflicts = count_conflicts(positions, CONFLICT_RADIUS)
print("Drones in conflict: {}".format(conflicts))
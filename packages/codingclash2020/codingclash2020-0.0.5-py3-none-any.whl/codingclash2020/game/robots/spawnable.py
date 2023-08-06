from ..helpers import dist
from .robot import Robot

class Spawnable(Robot):
    def __init__(self, max_spawn_count, spawn_costs, spawn_radius):
        self.spawnable = True
        self.max_spawn_count = max_spawn_count
        self.costs = spawn_costs
        self.spawn_radius = spawn_radius
        self.num_spawned = 0


    def run(self):
        self.num_spawned = 0


    def can_spawn(self, robot_type, location):
        if not self.can_perform_action():
            return False, "Robot is currently stunned"
        if self.attacked or self.moved:
            return False, "Robot already performed and action this turn"
        if self.num_spawned >= self.max_spawn_count:
            return False, "Robot already spawned its max amount of other robots this turn"
        if robot_type not in self.costs:
            return False, "Robot of type {} cannot spawn robot of type {}".format(self.type, robot_type)
        if dist(self.location, location) > self.spawn_radius:
            return False, "Location of {} is farther than the robot at {} can spawn".format(location, self.location)
        if self.team.oil < self.costs[robot_type]:
            return False, "The robot's team doesn't have enough oil to spawn a robot of type {}".format(robot_type)
        return True, None


    def spawn(self, robot_type, target_location):
        self.team.oil -= self.costs[robot_type]
        self.spawned = True
        self.num_spawned += 1

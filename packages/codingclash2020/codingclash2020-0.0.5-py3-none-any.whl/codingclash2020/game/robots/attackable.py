from ..helpers import dist
from .robot import Robot

class Attackable(Robot):
    def __init__(self, damage, attack_range, attack_cost, attack_aoe):
        self.attackable = True
        self.damage = damage
        self.attack_range = attack_range
        self.attack_cost = attack_cost
        self.attack_aoe = attack_aoe


    def run(self):
        pass


    def can_attack(self, target_robots):
        if not self.can_perform_action():
            return [], "Robot is currently stunned"
        if self.attacked or self.moved or self.spawned:
            return [], "Robot already performed some other action this turn"
        if self.team.oil < self.attack_cost:
            return [], "The robot's team doesn't have enough oil to attack"
        filtered = []
        for target in target_robots:
            if dist(self.location, target.location) <= self.attack_range:
                filtered.append(target)
        return filtered, None


    def attack(self):
        self.team.oil -= self.attack_cost
        self.attacked = True

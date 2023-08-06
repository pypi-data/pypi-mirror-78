from ..helpers import dist

class Robot:
    def __init__(self, id, location, team, robot_type, health, sense_range):
        self.id = id
        self.location = location
        self.team = team
        self.type = robot_type
        self.health = health
        self.sense_range = sense_range
        self.performed_action = False
        self.added_blockchain = False
        self.spawnable = False
        self.moveable = False
        self.attackable = False
        self.stun_rounds = 0
        self.attacked, self.moved, self.spawned = False, False, False


    def run(self):
        self.performed_action = False
        self.added_blockchain = False
        if self.stun_rounds > 0:
            self.stun_rounds -= 1
        self.attacked, self.moved, self.spawned = False, False, False


    def can_perform_action(self):
        return self.stun_rounds == 0


    def can_sense_location(self, location: tuple):
        return dist(self.location, location) <= self.sense_range

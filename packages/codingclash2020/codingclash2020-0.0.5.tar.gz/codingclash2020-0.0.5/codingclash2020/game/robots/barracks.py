from .. import constants as GameConstants
from ..robot_type import RobotType
from ..helpers import dist
from .robot import Robot
from .spawnable import Spawnable

class Barracks(Spawnable, Robot):
    def __init__(self, id, location, team):
        Robot.__init__(self, id,
                         location,
                         team, 
                         RobotType.BARRACKS, 
                         GameConstants.BARRACKS_HEALTH, 
                         GameConstants.BARRACKS_SENSE_RANGE)
        costs = {
            RobotType.GUNNER: GameConstants.GUNNER_COST,
            RobotType.TANK: GameConstants.TANK_COST,
            RobotType.GRENADER: GameConstants.GRENADER_COST,
        }
        Spawnable.__init__(self, GameConstants.BARRACKS_MAX_SPAWNS, costs, GameConstants.BARRACKS_SPAWN_RADIUS)


    def run(self):
        Robot.run(self)
        Spawnable.run(self)

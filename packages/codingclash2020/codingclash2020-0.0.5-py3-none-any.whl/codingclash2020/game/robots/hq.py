from .. import constants as GameConstants
from ..robot_type import RobotType
from ..helpers import dist
from .robot import Robot
from .spawnable import Spawnable

class HQ(Spawnable, Robot):
    def __init__(self, id, location, team):
        Robot.__init__(self, id,
                         location,
                         team, 
                         RobotType.HQ, 
                         GameConstants.HQ_HEALTH, 
                         GameConstants.HQ_SENSE_RANGE)
        costs = {
            RobotType.BUILDER: GameConstants.BUILDER_COST,
        }
        Spawnable.__init__(self, GameConstants.HQ_MAX_SPAWNS, costs, GameConstants.HQ_SPAWN_RADIUS)


    def run(self):
        Robot.run(self)
        Spawnable.run(self)
        self.team.oil += GameConstants.HQ_OIL_PRODUCTION

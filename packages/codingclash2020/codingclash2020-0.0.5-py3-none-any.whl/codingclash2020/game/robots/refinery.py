from .. import constants as GameConstants
from ..robot_type import RobotType
from ..helpers import dist
from .robot import Robot
from .spawnable import Spawnable

class Refinery(Spawnable, Robot):
    def __init__(self, id, location, team):
        Robot.__init__(self, id,
                         location,
                         team, 
                         RobotType.REFINERY, 
                         GameConstants.REFINERY_HEALTH, 
                         GameConstants.REFINERY_SENSE_RANGE)


    def run(self):
        Robot.run(self)
        Spawnable.run(self)
        self.team.oil += GameConstants.REFINERY_PRODUCTION

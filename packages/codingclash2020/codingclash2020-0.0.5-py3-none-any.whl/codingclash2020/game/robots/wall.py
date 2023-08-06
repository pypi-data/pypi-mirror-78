from .. import constants as GameConstants
from ..robot_type import RobotType
from ..helpers import dist
from .robot import Robot

class NoneTeam():
    def __init__(self):
        self.color = None

class Wall(Robot):
    def __init__(self, id, location):
        Robot.__init__(self, id,
                         location,
                         NoneTeam(), 
                         RobotType.WALL, 
                         GameConstants.WALL_HEALTH, 
                         -1)


    def run(self):
        Robot.run(self)

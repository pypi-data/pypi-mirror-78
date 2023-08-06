from .. import constants as GameConstants
from ..robot_type import RobotType
from ..helpers import dist
from .robot import Robot
from .attackable import Attackable

class Turret(Attackable, Robot):
    def __init__(self, id, location, team):
        Robot.__init__(self, id,
                         location,
                         team, 
                         RobotType.TURRET, 
                         GameConstants.TURRET_HEALTH, 
                         GameConstants.TURRET_SENSE_RANGE)
        Attackable.__init__(self, GameConstants.TURRET_DAMAGE, GameConstants.TURRET_ATTACK_RANGE, GameConstants.TURRET_ATTACK_COST, GameConstants.TURRET_AOE)


    def run(self):
        Robot.run(self)
        Attackable.run(self)

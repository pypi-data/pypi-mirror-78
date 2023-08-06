from .. import constants as GameConstants
from ..robot_type import RobotType
from ..helpers import dist
from .robot import Robot
from .moveable import Moveable
from .attackable import Attackable

class Tank(Moveable, Attackable, Robot):
    def __init__(self, id, location, team):
        Robot.__init__(self, id,
                         location,
                         team, 
                         RobotType.TANK, 
                         GameConstants.TANK_HEALTH, 
                         GameConstants.TANK_SENSE_RANGE)
        Moveable.__init__(self, GameConstants.TANK_SPEED)
        Attackable.__init__(self, GameConstants.TANK_DAMAGE, GameConstants.TANK_ATTACK_RANGE, GameConstants.TANK_ATTACK_COST, GameConstants.TANK_AOE)


    def run(self):
        Robot.run(self)
        Moveable.run(self)
        Attackable.run(self)

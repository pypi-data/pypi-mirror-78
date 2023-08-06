from .. import constants as GameConstants
from ..robot_type import RobotType
from ..helpers import dist
from .robot import Robot
from .moveable import Moveable
from .attackable import Attackable

class Gunner(Moveable, Attackable, Robot):
    def __init__(self, id, location, team):
        Robot.__init__(self, id,
                         location,
                         team, 
                         RobotType.GUNNER, 
                         GameConstants.GUNNER_HEALTH, 
                         GameConstants.GUNNER_SENSE_RANGE)
        Moveable.__init__(self, GameConstants.GUNNER_SPEED)
        Attackable.__init__(self, GameConstants.GUNNER_DAMAGE, GameConstants.GUNNER_ATTACK_RANGE, GameConstants.GUNNER_ATTACK_COST, GameConstants.GUNNER_AOE)
    

    def run(self):
        Robot.run(self)
        Moveable.run(self)
        Attackable.run(self)

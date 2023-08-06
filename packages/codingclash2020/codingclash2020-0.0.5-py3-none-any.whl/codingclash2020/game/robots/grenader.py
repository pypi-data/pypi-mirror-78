from .. import constants as GameConstants
from ..robot_type import RobotType
from ..helpers import dist
from .robot import Robot
from .moveable import Moveable
from .attackable import Attackable
from .stunnable import Stunnable

class Grenader(Moveable, Attackable, Stunnable, Robot):
    def __init__(self, id, location, team):
        Robot.__init__(self, id,
                         location,
                         team, 
                         RobotType.GRENADER, 
                         GameConstants.GRENADER_HEALTH, 
                         GameConstants.GRENADER_SENSE_RANGE)
        Moveable.__init__(self, GameConstants.GRENADER_SPEED)
        Attackable.__init__(self, GameConstants.GRENADER_DAMAGE_DAMAGE, GameConstants.GRENADER_DAMAGE_RANGE, GameConstants.GRENADER_DAMAGE_COST, GameConstants.GRENADER_DAMAGE_AOE)
        Stunnable.__init__(self, GameConstants.GRENADER_STUN_TURNS, GameConstants.GRENADER_STUN_RANGE, GameConstants.GRENADER_STUN_COST, GameConstants.GRENADER_STUN_AOE)
    

    def run(self):
        Robot.run(self)
        Moveable.run(self)
        Attackable.run(self)
        Stunnable.run(self)

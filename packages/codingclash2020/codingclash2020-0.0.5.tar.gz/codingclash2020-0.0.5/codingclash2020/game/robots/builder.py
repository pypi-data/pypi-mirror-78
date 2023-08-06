from .. import constants as GameConstants
from ..robot_type import RobotType
from ..helpers import dist
from .robot import Robot
from .moveable import Moveable
from .spawnable import Spawnable

class Builder(Spawnable, Moveable, Robot):
    def __init__(self, id, location, team):
        Robot.__init__(self, id,
                         location,
                         team, 
                         RobotType.BUILDER, 
                         GameConstants.BUILDER_HEALTH, 
                         GameConstants.BUILDER_SENSE_RANGE)
        Moveable.__init__(self, GameConstants.BUILDER_SPEED)
        costs = {
            RobotType.TURRET: GameConstants.TURRET_COST,
            RobotType.BARRACKS: GameConstants.BARRACKS_COST,
            RobotType.REFINERY: GameConstants.REFINERY_COST,
            RobotType.WALL: GameConstants.WALL_COST
        }
        Spawnable.__init__(self, GameConstants.BUILDER_MAX_SPAWNS, costs, GameConstants.BUILDER_SPAWN_RADIUS)


    def run(self):
        Robot.run(self)
        Moveable.run(self)
        Spawnable.run(self)

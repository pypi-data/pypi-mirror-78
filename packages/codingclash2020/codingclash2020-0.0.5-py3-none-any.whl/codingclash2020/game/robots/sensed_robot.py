from ..robot_type import RobotType
from ..team_color import TeamColor

class SensedRobot:
    def __init__(self, robot_type: RobotType, team: TeamColor, location: tuple, health: int):
        self.type = robot_type
        self.team = team
        self.location = location
        self.health = health

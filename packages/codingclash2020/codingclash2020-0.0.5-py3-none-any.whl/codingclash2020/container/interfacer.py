from ..game.team_color import TeamColor
from ..game.robot_type import RobotType
from ..game import constants as GameConstants

from RestrictedPython import compile_restricted as compile

from RestrictedPython import safe_builtins
from RestrictedPython import limited_builtins
from RestrictedPython import utility_builtins


def import_call(name, globals=None, locals=None, fromlist=(), level=0, caller='Interfacer'):
    assert(isinstance(name, str))
    if name == 'random':
        import random
        return random
    if name == 'math':
        import math
        return math
    raise Exception("Disallowed import call: {}".format(name))


class Interfacer:
    def __init__(self, moderator, code, robot, id):
        self.moderator = moderator
        self.code = code
        self.robot = robot
        self.id = id
        builts = {i: built[i] for built in [safe_builtins, limited_builtins, utility_builtins] for i in built}
        self.globals = {
            '__builtins__': builts,
            '__name__': '__main__'
            }
       
        # self.locals = self.globals
        # self.locals = {}
        # self.locals = {
        #     '__builtins__': __builtins__.copy(),
        #     '__name__': '__main__'
        #     }

        # Add extra builtins not included in RestrictedPython
        self.extra_builtins = {}
        self.extra_builtins['__import__'] = import_call
        self.extra_builtins['print'] = print
        self.extra_builtins['super'] = super
        self.extra_builtins['min'] = min
        self.extra_builtins['max'] = max
        self.extra_builtins['sorted'] = sorted
        
        for built in self.extra_builtins:
            self.globals['__builtins__'][built] = self.extra_builtins[built]


        self.game_methods = {
            'get_board_width': lambda : self.get_board_width(),
            'get_board_height': lambda : self.get_board_height(),
            'get_team': lambda : self.get_team(),
            'get_type': lambda : self.get_type(),
            'get_health': lambda : self.get_health(),
            'get_location': lambda : self.get_location(),
            'get_oil': lambda : self.get_oil(),
            'get_round_num': lambda : self.get_round_num(),
            'is_stunned': lambda : self.is_stunned(),
            'sense': lambda : self.sense(),
            'can_sense_location': lambda loc : self.can_sense_location(loc),
            'sense_location': lambda loc : self.sense_location(loc),
            'move': lambda loc : self.move(loc),
            'create': lambda robot_type, loc : self.create(robot_type, loc),
            'attack': lambda loc : self.attack(loc),
            'stun': lambda loc: self.stun(loc),
            'get_blockchain': lambda round_num : self.get_blockchain(round_num),
            'add_to_blockchain': lambda data : self.add_to_blockchain(data),
            'dlog': lambda msg : self.dlog(msg)
        }

        self.enums = {
            'RobotType': RobotType,
            'TeamColor': TeamColor,
            'GameConstants': GameConstants
        }

        # TODO: add print back to this
        self.disallowed_enums = []
#        self.disallowed_enums = ['print']

        for key in self.disallowed_enums:
            del self.globals['__builtins__'][key]

        for key in self.game_methods:
            self.globals['__builtins__'][key] = self.game_methods[key]

        for key in self.enums:
            self.globals['__builtins__'][key] = self.enums[key]
        

    def init_code(self):
        exec(self.code, self.globals)

    def run(self):
        self.robot.run()
        # TODO: Also reimport libraries and reset GameConstants and whatnot every time
        code = self.globals['turn'].__code__
        exec(code, self.globals)

    ## Translation of moderator methods
    
    # Basic getter methods

    def get_board_width(self):
        return self.moderator.board_width

    def get_board_height(self):
        return self.moderator.board_height
    
    def get_team(self):
        return self.robot.team.color

    def get_type(self):
        return self.robot.type

    def get_health(self):
        return self.robot.health

    def get_location(self):
        return self.robot.location
    
    def get_oil(self):
        return self.robot.team.oil
    
    def get_round_num(self):
        return self.moderator.round_num
    
    def is_stunned(self):
         return self.robot.stun_rounds > 0

    # Sensing

    def sense(self):
        return self.moderator.sense(self.robot)

    def sense_radius(self, radius):
        return self.moderator.sense(self.robot, radius)

    def can_sense_location(self, location):
        return self.moderator.can_sense_location(self.robot, location)

    def sense_location(self, location):
        sensed = self.moderator.sense_location(self.robot, location)
        if not sensed:
            raise Exception("The location {} that you're trying to sense is either out of bounds or not within your sensor range".format(location))
        return sensed

    # Creating robots

    def create(self, robot_type, location):
        return self.moderator.create(self.robot, robot_type, self.robot.team, location)

    # Robot actions (can only do one per turn)

    def move(self, location):
        return self.moderator.move(self.robot, location)
    
    def attack(self, location):
        return self.moderator.attack(self.robot, location)
    
    def stun(self, location):
        return self.moderator.stun(self.robot, location)

    # Blockchain

    def add_to_blockchain(self, data):
        return self.moderator.add_to_blockchain(self.robot, data)

    def get_blockchain(self, round_num):
        return self.moderator.get_blockchain(self.robot, round_num)

    # Logging

    def dlog(self, message):
        self.moderator.dlog(self.robot, message)

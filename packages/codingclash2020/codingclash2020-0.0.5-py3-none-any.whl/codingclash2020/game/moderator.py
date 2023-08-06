import random
from .team import Team
from .team_color import TeamColor
from .helpers import dist, squares_within_distance, in_between
from .robot_type import RobotType
from . import constants as GameConstants
from .robots import Robot, HQ, Refinery, Barracks, Turret, Builder, Gunner, Tank, Grenader, SensedRobot, Wall

ROBOT_MAP = {
    RobotType.REFINERY: Refinery,
    RobotType.BARRACKS: Barracks,
    RobotType.TURRET: Turret,
    RobotType.BUILDER: Builder,
    RobotType.GUNNER: Gunner,
    RobotType.TANK: Tank,
    RobotType.GRENADER: Grenader,
    RobotType.WALL: Wall,
}


class Moderator:
    def __init__(self, map_filename):
        self.ids = set()
        self.red, self.blue = Team(TeamColor.RED), Team(TeamColor.BLUE)
        self.load_map(map_filename)
        self.robots = [self.HQs[TeamColor.RED], self.HQs[TeamColor.BLUE]]
        self.game_over = False
        self.winner = None
        self.debug, self.info = [], []
        self.ledger = []
        self.round_num = -1

    def load_map(self, map_name):
        self.board = []
        self.HQs = {}
        file = open("maps/" + map_name + ".map")
        lines = [line.strip() for line in file]
        self.board_height = len(lines)
        self.board_width = len(lines[0])
        # Allow only square maps for now, NOTE: We should allow rectangle maps eventually
        assert(self.board_width == self.board_height)
        self.board = [[RobotType.NONE for i in range(self.board_height)] for j in range(self.board_width)]
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == 'H':
                    self.HQs[TeamColor.RED] = self.create_hq(self.red, (x,y))
                elif char == 'h':
                    self.HQs[TeamColor.BLUE] = self.create_hq(self.blue, (x,y))
                elif char == 'w':
                    id = random.random()
                    self.ids.add(id)
                    wall = Wall(id, (x,y))
                    self.put_robot(wall, (x,y))



    def update_info(self):
        for robot in self.robots:
            # Format: [INFO] [ID] X Y HEALTH
            self.info.append(
                "[INFO] [{}] {} {} {}".format(robot.id, robot.location[0], robot.location[1], robot.health))
        if self.ledger:
            self.info.append("[BCHAIN] {}".format(';'.join([str(i) for i in self.ledger[-1]])))

    def start_next_round(self):
        self.round_num += 1
        self.ledger.append([])

    ## Helper methods

    def get_robot(self, location: tuple):
        return self.board[location[0]][location[1]]

    def put_robot(self, robot: Robot, location: tuple):
        self.board[location[0]][location[1]] = robot

    def remove_robot(self, location: tuple):
        self.board[location[0]][location[1]] = RobotType.NONE

    def inbounds(self, location: tuple):
        return location[0] >= 0 and location[0] < self.board_width and location[1] >= 0 and location[
            1] < self.board_height

    def location_occupied(self, location: tuple) -> bool:
        if not self.inbounds(location):
            return False
        return self.get_robot(location) != RobotType.NONE

    ## Game State methods (player inputs)

    def dlog(self, robot: Robot, message: str):
        self.debug.append("[DLOG] [{}] {}".format(robot.id, message))

    def sense(self, robot: Robot):
        sense_range = robot.sense_range
        squares = squares_within_distance(sense_range)
        robot_location = robot.location
        sensed_list = []

        for dx, dy in squares:
            loc = (robot_location[0] + dx, robot_location[1] + dy)
            sensed = self.sense_location(robot, loc)
            if sensed and sensed.type != RobotType.NONE:
                sensed_list.append(sensed)

        return sensed_list

    def sense_radius(self, robot: Robot, radius):
        sense_range = radius
        if sense_range > robot.sense_range:
            # Can't sense outside of your sensor range
            return None
        squares = squares_within_distance(sense_range)
        robot_location = robot.location
        sensed_list = []

        for dx, dy in squares:
            loc = (robot_location[0] + dx, robot_location[1] + dy)
            sensed = self.sense_location(robot, loc)
            if sensed and sensed.type != RobotType.NONE:
                sensed_list.append(sensed)

        return sensed_list


    def can_sense_location(self, robot: Robot, location: tuple):
        if not self.inbounds(location):
            return False
        return robot.can_sense_location(location)


    def sense_location(self, robot: Robot, location: tuple):
        if not self.can_sense_location(robot, location):
            # The location you are trying to sense is not within your sensor range
            return None
        robot = self.get_robot(location)
        sensed = None
        if robot == RobotType.NONE:
            sensed = SensedRobot(RobotType.NONE, None, location, None)
        else:
            sensed = SensedRobot(robot.type, robot.team.color, robot.location, robot.health)
        return sensed

    ## Game Action methods (player outputs)

    """
    Creates a new robot in a specified location.
    Returns the True if the robot moved successfully, otherwise False
    """

    def move(self, robot: Robot, location: tuple) -> bool:
        if not robot.moveable:
            raise Exception("Robot of type {} is not moveable".format(robot.type))
        if self.get_robot(location) != RobotType.NONE:
            raise Exception("Robot is present at {} location".format(location))
        if not self.inbounds(location):
            raise Exception("Given location of {} is not inbounds".format(location))

        can_move, reason = robot.can_move(location)
        if not can_move:
            raise Exception(reason)

        curr_location = robot.location
        robot.move(location)
        self.put_robot(robot, location)
        self.remove_robot(curr_location)
        return True

    def create_hq(self, team: Team, location: tuple) -> HQ:
        id = random.random()
        hq = HQ(id, location, team)
        self.put_robot(hq, location)
        self.ids.add(id)
        return hq

    """
    Creates a new robot in a specified location.
    Returns the robot object if the creation is valid, otherwise returns None
    """

    def create(self, robot: Robot, robot_type: RobotType, team: Team, location: tuple) -> bool:
        if not robot.spawnable:
            raise Exception("Robot of type {} cannot spawn other robots".format(robot.type))
        if not self.inbounds(location):
            raise Exception("Target creation location of {} is not inbounds".format(location))
        if self.location_occupied(location):
            raise Exception("Target creation location of {} is occupied".format(location))
        can_spawn, reason = robot.can_spawn(robot_type, location)

        if not can_spawn:
            raise Exception(reason)

        robot.spawn(robot_type, location)

        # Spawn the new robot
        assert(robot_type in ROBOT_MAP)
        new_robot_type = ROBOT_MAP[robot_type]
        id = random.random()
        #print(new_robot_type)
        if robot_type != RobotType.WALL:
            new_robot = new_robot_type(id, location, team)
        else: 
            new_robot = new_robot_type(id, location)

        self.ids.add(id)
        self.put_robot(new_robot, location)
        if new_robot.type != RobotType.WALL:
            self.robots.append(new_robot)
        return True

    """
    Attacks the robot in a specified location.
    Returns True if the attack was possible, else False
    """

    def attack(self, robot: Robot, target_location: tuple) -> bool:
        if not self.inbounds(target_location):
            raise Exception("Target attack location of {} is not on the map".format(target_location))
        if not robot.attackable:
            raise Exception("Robot of type {} can't attack".format(robot.type))

        target_robots = []
        squares = squares_within_distance(robot.attack_aoe)
        for dx, dy in squares:
            loc = (target_location[0] + dx, target_location[1] + dy)
            target_robot = self.get_robot(loc)
            if target_robot == RobotType.NONE:
                continue
            if target_robot.team.color == robot.team.color:
                continue
            worked = True
            for i in self.sense(robot):
                if i.team != robot.team.color and in_between(robot.location, loc, i.location):
                    worked = False
            if not worked:
                continue
            target_robots.append(target_robot)
        filtered, reason = robot.can_attack(target_robots)
        if reason:
            raise Exception(reason)
        if not filtered:
            raise Exception("No valid enemy robots to attack around that location {}".format(target_location))

        # Actually attack
        robot.attack()
        for target_robot in filtered:
            target_robot.health -= robot.damage
            if target_robot.health <= 0:
                self.kill(target_robot)

    """
    Stuns the robot in a specified location.
    Returns True if the stun was possible, else False
    """

    def stun(self, robot: Robot, target_location: tuple) -> bool:
        if not robot.stunnable:
            raise Exception("Robot of type {} can't stun".format(robot.type))
        if not self.inbounds(target_location):
            raise Exception("Target attack location of {} is not on the map".format(target_location))

        target_robots = []
        squares = squares_within_distance(robot.stun_aoe)
        for dx, dy in squares:
            loc = (target_location[0] + dx, target_location[1] + dy)
            worked = True
            target_robot = self.get_robot(loc)
            if target_robot == RobotType.NONE:
                worked = False
            if target_robot.team.color == robot.team.color:
                worked = False
            for i in self.sense(robot):
                if i.team.color != robot.team.color and in_between(robot.location, loc, i.location):
                    worked = False
            if worked:
                target_robots.append(target_robot)
        filtered, reason = robot.can_stun(target_robots)
        if reason:
            raise Exception(reason)
        if not filtered:
            raise Exception("No valid enemy robots to stun around that location {}".format(target_location))

        # Actually attack
        robot.stun()
        for target_robot in filtered:
            target_robot.stun_rounds += robot.stun_turns

    """
    Wipes a robot out of existence
    """

    def kill(self, robot: Robot):
        if robot.type != RobotType.WALL:
            try:
                self.robots.remove(robot)
            except:
                raise Exception("Robot that you're trying to kill not found: " + str(robot.id))
        if robot.type == RobotType.HQ:
            self.game_over = True
            # print("Killed", robot.team)
            self.winner = TeamColor.RED if robot.team.color == TeamColor.BLUE else TeamColor.BLUE
        location = robot.location
        self.remove_robot(location)

    """
    Adds message to blockchain board
    @param data: a list of length 5 w/ bytes (ints from 0 to 255) 
    """

    def add_to_blockchain(self, robot: Robot, data: list):
        if robot.added_blockchain:
            raise Exception("Robot can only add to blockchain once per round")
        if not isinstance(data, list) or not isinstance(data[0], int) or len(
                data) != GameConstants.BLOCKCHAIN_BYTE_COUNT:
            raise Exception(
                "Blockchain requires a list of ints of length {}".format(GameConstants.BLOCKCHAIN_BYTE_COUNT))
        for byt in data:
            if byt > GameConstants.BLOCKCHAIN_MAX_NUM_SIZE or byt < GameConstants.BLOCKCHAIN_MIN_NUM_SIZE:
                raise Exception("Blockchain ints must be between {} and {}, but received int of {}".format(
                    GameConstants.BLOCKCHAIN_MIN_NUM_SIZE, GameConstants.BLOCKCHAIN_MAX_NUM_SIZE, byt))

        self.ledger[-1].append(data)

    def get_blockchain(self, robot: Robot, round_num: int):
        if round_num < 0: 
            raise Exception("There's no blockchain prior to the first round")
        if round_num >= len(self.ledger) - 1:
            raise Exception("Round {} has not finished yet".format(round_num))
        return self.ledger[round_num].copy()

    def get_round_num(self, robot: Robot):
        return self.round_num

    def run_tiebreak(self):
        if self.winner:
            return

        red_health, blue_health = self.HQs[TeamColor.RED].health, self.HQs[TeamColor.BLUE].health
        self.winner = TeamColor.RED if red_health > blue_health else TeamColor.BLUE if blue_health > red_health else None
        if self.winner is not None:
            return

        red_troops, blue_troops = 0, 0
        for robot in self.robots:
            if robot.team.color == TeamColor.RED:
                red_troops += 1
            if robot.team.color == TeamColor.BLUE:
                blue_troops += 1

        self.winner = TeamColor.RED if red_troops > blue_troops else TeamColor.BLUE if blue_troops > red_troops else None
        if self.winner is not None:
            return

        red_oil, blue_oil = self.red.oil, self.blue.oil
        self.winner = TeamColor.RED if red_oil > blue_oil else TeamColor.BLUE if blue_oil > red_oil else None
        if self.winner is not None:
            return

        coinflip = random.randint(0, 1)
        self.winner = TeamColor.RED if coinflip else TeamColor.BLUE

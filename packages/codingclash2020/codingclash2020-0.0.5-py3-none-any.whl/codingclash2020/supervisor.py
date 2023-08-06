# Local imports
from .game.team_color import TeamColor
from .game.moderator import Moderator
from .game.robot_type import RobotType
from .container.interfacer import Interfacer
from .game import constants as GameConstants

# Imports used for setting time limit on method
import signal
from contextlib import contextmanager

# Exception when time limit is exceeded
class TimeoutException(Exception): pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
#    signal.alarm(seconds)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class Supervisor:
    def __init__(self, filename1, filename2, map_filename='empty'):
        self.filename1 = filename1
        self.filename2 = filename2
        self.code1 = self.read_code(filename1)
        self.code2 = self.read_code(filename2)
        self.moderator = Moderator(map_filename)
        self.interfacers = []
        self.robot_ids = set()
        # Used for visualization
        self.robot_letter_map = {RobotType.BARRACKS: "S", RobotType.BUILDER: "B", RobotType.GUNNER: "G", RobotType.GRENADER: "E", RobotType.HQ: "H", RobotType.REFINERY: "R", RobotType.TANK: "T", RobotType.TURRET: "U"}
        self.robot_to_str = {}
        for robot_type in self.robot_letter_map:
            letter = self.robot_letter_map[robot_type]
            self.robot_to_str[(TeamColor.RED, robot_type)] = letter.upper()
            self.robot_to_str[(TeamColor.BLUE, robot_type)] = letter.lower()
        self.robot_to_str[(None, RobotType.WALL)] = "W"
        self.robot_to_str[RobotType.NONE] = "n"
        self.boards = []
        self.quiet = False


    def read_code(self, filename):
        file = open(filename, 'r')
        code = file.read().strip()
        lines = code.split("\n")
        new_lines = []
        for line in lines:
            if "from stubs import" not in line:
                new_lines.append(line)
        code = '\n'.join(new_lines)
        return code


    def update_interfacers(self):
        for robot in self.moderator.robots:
            if robot.id in self.robot_ids:
                continue
            code = self.code1 if robot.team.color == TeamColor.BLUE else self.code2
            interfacer = Interfacer(self.moderator, code, robot, robot.id)
            interfacer.init_code()
            self.interfacers.append(interfacer)
            self.robot_ids.add(robot.id)

    
    def run_turn(self):
        self.update_interfacers()
        to_remove = []
        for interfacer in self.interfacers:
            if interfacer.robot not in self.moderator.robots:
                # The robot died this turn
                to_remove.append(interfacer)
                continue
            try:
                with time_limit(GameConstants.TIME_LIMIT):
                    interfacer.run()
            except Exception as e:
                error_str = "[ERROR] [{}] [{}] [{}]: {}".format(interfacer.robot.id, interfacer.robot.team.color, interfacer.robot.type, e)
                if not self.quiet:
                    print(error_str)
                self.errors.append(error_str)
            signal.alarm(0)

            if self.moderator.game_over:
                break

        for interfacer in to_remove:
            self.interfacers.remove(interfacer)


    def run(self, max_rounds=GameConstants.DEFAULT_NUM_ROUNDS):
        self.boards = [[row.copy() for row in self.moderator.board]]
        self.moderator.update_info()
        self.comments = {0: self.moderator.info + self.moderator.debug.copy()}
        self.errors = []
        for i in range(max_rounds):
            if not self.quiet:
                print("Turn", i)
            self.moderator.debug, self.moderator.info, self.errors = [], [], []
            self.moderator.start_next_round()
            self.run_turn()
            self.moderator.update_info()
            self.comments[i + 1] = self.moderator.info + self.moderator.debug.copy() + self.errors
            self.boards.append([row.copy() for row in self.moderator.board])
            if self.moderator.game_over:
                break
        self.moderator.run_tiebreak()
        file_winner = self.filename1 if self.moderator.winner == TeamColor.BLUE else self.filename2 if self.moderator.winner == TeamColor.RED else None
        if not self.quiet:
            print("Winner: {}".format(file_winner if file_winner else "Tie"))
        return self.moderator.winner


    def get_replayable_board(self, moderator_board):
        board = []
        for row in moderator_board:
            temp = []
            for robot in row:
                piece = self.robot_to_str[RobotType.NONE]
                if robot != RobotType.NONE:
                    piece = self.robot_to_str[(robot.team.color, robot.type)]
                temp.append(piece)
            board.append(temp)
        return board


    def board_to_string(self, board):
        bout = [j for sub in board for j in sub]
        return "#"+"".join(bout)


    def get_replay(self):
        #print(self.boards)
        data = []
        data.append("|blue: {}".format(self.filename1))
        data.append("|red: {}".format(self.filename2))
        for i, board in enumerate(self.boards):
            data.append(self.board_to_string(self.get_replayable_board(board)))
            if i in self.comments:
                for comment in self.comments[i]:
                    data.append(comment)

        data.append("|Winner: {}".format(self.filename1 if self.moderator.winner == TeamColor.BLUE else self.filename2))
        data.append("|Winner color: {}".format("blue" if self.moderator.winner == TeamColor.BLUE else "red"))

        return "\n".join(data)

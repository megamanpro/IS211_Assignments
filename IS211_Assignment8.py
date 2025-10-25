import argparse
import random
import time
import sys

WIN_SCORE = 100
TIME_LIMIT_SECONDS = 60

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def take_turn(self, game):
        raise NotImplementedError

class HumanPlayer(Player):
    def take_turn(self, game):
        turn_total = 0
        while True:
            print(f"\n{self.name}'s turn. Score: {self.score}, Turn total: {turn_total}")
            choice = input("Roll or hold? (r/h): ").strip().lower()
            if choice not in ('r', 'h'):
                print("Enter 'r' to roll or 'h' to hold.")
                continue
            if choice == 'r':
                roll = game.roll_die()
                print(f"{self.name} rolled: {roll}")
                if roll == 1:
                    print("Rolled a 1. Turn over, no points added.")
                    return
                turn_total += roll
            else:
                self.score += turn_total
                print(f"{self.name} holds. New score: {self.score}")
                return

class ComputerPlayer(Player):
    def take_turn(self, game):
        turn_total = 0
        print(f"\n{self.name}'s turn. Score: {self.score}")
        while True:
            threshold = min(25, WIN_SCORE - self.score)
            if turn_total >= threshold:
                self.score += turn_total
                print(f"{self.name} holds with turn total {turn_total}. New score: {self.score}")
                return
            roll = game.roll_die()
            print(f"{self.name} rolled: {roll}")
            if roll == 1:
                print(f"{self.name} rolled a 1. Turn over, no points added.")
                return
            turn_total += roll

class PlayerFactory:
    @staticmethod
    def create_player(player_type: str, name: str) -> Player:
        pt = player_type.lower()
        if pt == "human":
            return HumanPlayer(name)
        if pt == "computer":
            return ComputerPlayer(name)
        raise ValueError(f"Unknown player type: {player_type}")

class Game:
    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]

    def roll_die(self) -> int:
        return random.randint(1, 6)

    def play(self):
        while all(p.score < WIN_SCORE for p in self.players):
            for player in self.players:
                player.take_turn(self)
                if player.score >= WIN_SCORE:
                    print(f"\n{player.name} wins with {player.score} points!")
                    return player
        return None

class TimedGameProxy:
    def __init__(self, game: Game, time_limit_seconds: int = TIME_LIMIT_SECONDS):
        self.game = game
        self.start_time = None
        self.time_limit_seconds = time_limit_seconds

    def roll_die(self):
        return self.game.roll_die()

    def play(self):
        self.start_time = time.time()
        while all(p.score < WIN_SCORE for p in self.game.players):
            if time.time() - self.start_time > self.time_limit_seconds:
                winner = max(self.game.players, key=lambda p: p.score)
                print(f"\nTime's up! {winner.name} wins with {winner.score} points.")
                return winner
            for player in self.game.players:
                if time.time() - self.start_time > self.time_limit_seconds:
                    winner = max(self.game.players, key=lambda p: p.score)
                    print(f"\nTime's up! {winner.name} wins with {winner.score} points.")
                    return winner
                player.take_turn(self.game)
                if player.score >= WIN_SCORE:
                    print(f"\n{player.name} wins with {player.score} points!")
                    return player
        return None

def parse_args_with_defaults():
    parser = argparse.ArgumentParser(description="Play Pig with Factory and Proxy patterns.")
    parser.add_argument("--player1", choices=["human", "computer"], help="Type for player1")
    parser.add_argument("--player2", choices=["human", "computer"], help="Type for player2")
    parser.add_argument("--timed", action="store_true", help="Enable timed mode (60s)")
    args = parser.parse_args()

    # Provide defaults when running without args (convenience for PyCharm)
    if args.player1 is None or args.player2 is None:
        print("No --player1/--player2 provided, defaulting to: --player1 human --player2 computer")
        args.player1 = args.player1 or "human"
        args.player2 = args.player2 or "computer"
    return args

def main():
    args = parse_args_with_defaults()
    p1 = PlayerFactory.create_player(args.player1, "Player 1")
    p2 = PlayerFactory.create_player(args.player2, "Player 2")
    base_game = Game(p1, p2)

    if args.timed:
        game = TimedGameProxy(base_game)
    else:
        game = base_game
    try:
        game.play()
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()

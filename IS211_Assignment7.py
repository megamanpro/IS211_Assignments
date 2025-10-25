import random

random.seed(0)

class Die:
    def __init__(self, sides=6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

class PigGame:
    WIN_SCORE = 100

    def __init__(self, player_names):
        if len(player_names) < 2:
            raise ValueError("At least two players required")
        self.players = [Player(n) for n in player_names]
        self.die = Die()
        self.current_player_idx = 0

    def current_player(self):
        return self.players[self.current_player_idx]

    def next_player(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def play_turn(self):
        player = self.current_player()
        turn_total = 0

        while True:
            print(f"\n{player.name}'s turn. Current game score: {player.score}. Turn total so far: {turn_total}.")
            choice = input("Enter 'r' to roll or 'h' to hold: ").strip().lower()
            if choice not in ('r', 'h'):
                print("Invalid input. Please enter 'r' to roll or 'h' to hold.")
                continue

            if choice == 'r':
                roll = self.die.roll()
                print(f"{player.name} rolled: {roll}.")
                if roll == 1:
                    print("Rolled a 1. Turn ends with no points added.")
                    turn_total = 0
                    break
                else:
                    turn_total += roll
                    print(f"Turn total is now {turn_total}.")
                    continue
            else:
                player.score += turn_total
                print(f"{player.name} holds. {turn_total} points added to game score.")
                turn_total = 0
                break

    def play(self):
        print("Starting Pig Game. First to reach 100 or more wins.")
        while True:
            self.play_turn()
            player = self.current_player()
            print(f"{player.name}'s total score: {player.score}.")
            if player.score >= PigGame.WIN_SCORE:
                print(f"\n{player.name} wins with {player.score} points! Game over.")
                break
            self.next_player()

if __name__ == "__main__":
    print("Two-player Pig game.")
    name1 = input("Enter name for Player 1 (leave blank for 'Player 1'): ").strip() or "Player 1"
    name2 = input("Enter name for Player 2 (leave blank for 'Player 2'): ").strip() or "Player 2"
    game = PigGame([name1, name2])
    game.play()

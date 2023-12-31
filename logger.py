from typing import Tuple


def logMove(player: bool, indexFrom: int, indexTo: int):
    print(f"Player {'Black' if player else 'White'} moved their checker from triangle {'occupation' if indexFrom < 0 else indexFrom} to triangle {indexTo}.")


def logDice(player: bool, result: Tuple[int, int]):
    print(f"Player {'Black' if player else 'White'} just rolled {result[0]} and {result[1]}.")


def logWinner(player: bool):
    print(f"{'Black' if player else 'White'} player won!")


def logOccupy(attacker: bool, checker: int):
    print(f"Player {'Black' if attacker else 'White' } occupied {'White' if attacker else 'Black'} checker at triangle {checker}.")


def logSkipMove(player: bool):
    print(f"Player {'Black' if player else 'White'} skipped their move.")


def logMoveToHome(player: bool, index: int):
    print(f"Player {'Black' if player else 'White'} moved their checker from triangle {index} to their home.")


def logGameEnd(player: bool):
    print(f"Player {'Black' if player else 'White'} just won!")

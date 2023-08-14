from typing import Tuple


def logMove(player: bool, indexFrom: int, indexTo: int):
    print(f"Player {'Black' if player else 'White'} moved their checker from triangle {indexFrom} to triangle {indexTo}.")


def logDice(player: bool, result: Tuple[int, int]):
    print(f"Player {'Black' if player else 'White'} just rolled {result[0]} and {result[1]}")


def logWinner(player: bool):
    print(f"{'Black' if player else 'White'} player won!")

# core dice:
#   fury die on 1
#   void die on 5+
#   energy on 2+

# fury dice:
#   frenzy +1 on 1-3
#   frenzy +2 on 4-6

# void dice:
#   void die on 5+
#   always produce 1 energy

import random
from dataclasses import dataclass


@dataclass
class RollResult:
    values: list[int]
    faces: list[int]
    energy: int
    fury: int


class DicePool:
    def __init__(self) -> None:
        self.basic_dice_pool: int = 5
        self.void_dice_pool: int = 0
        self.fury_dice_pool: int = 0

    @staticmethod
    def counting_sort(rolled_dice_values: list[int]) -> tuple[list[int], list[int]]:
        # Create a count array to store the count of each number from 1 to 6
        count = [0] * 6

        # Count the occurrences of each number in the input array
        for num in rolled_dice_values:
            count[
                num - 1
            ] += 1  # Decrementing by 1 to map the numbers to the index range 0-5

        # Reconstruct the sorted array
        sorted_arr = []
        for i in range(6):
            sorted_arr.extend(
                [i + 1] * count[i]
            )  # Incrementing by 1 to map the index back to the numbers 1-6

        return sorted_arr, count

    @staticmethod
    def generate_values(n: int) -> list[int]:
        return [random.randint(1, 6) for _ in range(n)]

    @staticmethod
    def roll_dice(n: int) -> tuple[list[int], list[int]]:
        dice_rolls, face_counts = DicePool.counting_sort(DicePool.generate_values(n))
        return dice_rolls, face_counts

    def roll(self) -> RollResult:
        # roll basic dice, sort results
        # possible optimization: keep rolling dice between frames and keep a buffer of rolled dice

        # a rolling count that holds the remaining number of dice to roll.
        #   unrolled_dice decreases each pass by the number of dice rolled
        #   unrolled_dice increases each pass by the number of dice added/generated.
        unrolled_dice: int = self.basic_dice_pool
        rolled_dice_pool: list[int] = []
        rolled_dice_faces: list[int] = []
        accumulated_energy = 0
        accumulated_fury = 0

        while unrolled_dice > 0:
            # roll the dice we have so far
            sub_roll, faces = DicePool.roll_dice(unrolled_dice)
            rolled_dice_pool += sub_roll
            rolled_dice_faces += faces

            # decrease unrolled_dice by that amount
            unrolled_dice = -unrolled_dice

            # REMEMBER 0 INDEXING
            # these six-sided dice are functionally faced with 0,1,2,3,4,5

            # each 2+ generates energy for this turn
            accumulated_energy += faces[1] + faces[2] + faces[3] + faces[4] + faces[5]

            # each 1 generates fury
            accumulated_fury += faces[0]

            # each 5+ "blows up" - generates a temporary void die (again, 4+ for zero-indexing)
            added_void_dice = faces[4] + faces[5]  # faces[5-1] + faces[6-1]
            unrolled_dice += added_void_dice
            self.void_dice_pool += added_void_dice

        return RollResult(
            values=rolled_dice_pool,
            faces=rolled_dice_faces,
            energy=accumulated_energy,
            fury=accumulated_fury,
        )

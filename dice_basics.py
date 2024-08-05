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
from dataclasses import dataclass, field


@dataclass
class SortedPoolData:
    # This is intended to handle values between 1-6 but would work fine for artibrary values.

    # the given array of dice rolls, sorted least to greatest (values 1 through 6)
    sorted_values: list[int]

    # value_counts
    #   counts of each value - 1, because it's zero indexed.
    #   e.g. if the values rolled are [1, 1, 1, 1, 1]
    #   then value_counts will be [5, 0, 0, 0, 0] i.e. index 0 represents value 1
    value_counts: list[int]

    # greater_than_counts
    #   helps quickly answer the question "how many dice facings were value n or greater?"
    #   e.g. If the rolls were [1, 1, 4, 5, 6] than this array will be [5, 3, 3, 3, 2, 1] i.e.
    #       greater_than_counts[0] == "how many dice facings are 1 or greater?"
    #       greater_than_counts[1] == "how many dice facings are 2 or greater?"
    #       etc.
    gte_counts: list[int]



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
            # Decrementing by 1 to map the numbers to the index range 0-5
            count[num - 1] += 1

        # Reconstruct the sorted array
        sorted_arr = []
        for i in range(6):
            sorted_arr.extend(
                [i + 1] * count[i]
            )  # Incrementing by 1 to map the index back to the numbers 1-6

        # Calculate the gte_counts array
        gte_counts = [0] * 6
        cumulative_count = 0
        for i in range(5, -1, -1):  # Iterate from 5 down to 0
            cumulative_count += count[i]
            gte_counts[i] = cumulative_count

        return SortedPoolData(sorted_values=sorted_arr, value_counts=count, gte_counts=gte_counts)

    @staticmethod
    def generate_values(n: int) -> list[int]:
        return [random.randint(1, 6) for _ in range(n)]

    @staticmethod
    def roll_dice(n: int) -> SortedPoolData:
        return DicePool.counting_sort(DicePool.generate_values(n))

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
            sub_roll, faces, gte = DicePool.roll_dice(unrolled_dice)
            rolled_dice_pool += sub_roll
            rolled_dice_faces += faces

            # decrease unrolled_dice by that amount
            unrolled_dice = -unrolled_dice

            # REMEMBER 0 INDEXING
            # these six-sided dice are functionally faced with 0,1,2,3,4,5

            # each 2+ generates energy for this turn
            accumulated_energy += gte[1]

            # each 1 generates fury
            accumulated_fury += faces[0]

            # each 5+ "surges" - generates a temporary void die (again, 4+ for zero-indexing)
            added_void_dice = gte[4]  # 5+ (5-1 for indexing)
            unrolled_dice += added_void_dice
            self.void_dice_pool += added_void_dice

        return RollResult(
            values=rolled_dice_pool,
            faces=rolled_dice_faces,
            energy=accumulated_energy,
            fury=accumulated_fury,
        )

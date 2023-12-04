"""Solution to Day 3 challenge of the Advent of Code 2023."""

import operator
from typing import Literal, Optional

from icecream import ic

ENGLISH_SYMBOLS: list[str] = [
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    "-",
    "/",
    ":",
    ";",
    "<",
    "=",
    ">",
    "?",
    "@",
    "[",
    "\\",
    "]",
    "^",
    "_",
    "`",
    "{",
    "|",
    "}",
    "~",
]


def get_symbol_indexes(
    schematic: list[str], symbol: str | list[str]
) -> dict[int, list[int]]:
    """Return value is a dictionary whose keys are the line numbers in the schematic and whose values are the indexes at which there is a symbol on that line that is not a dot."""
    line_symbol_locs: dict[int, list[int]] = {}

    for line_num, line in enumerate(schematic):
        symbol_locs: list[int] = []
        for idx, char in enumerate(line):
            if char in symbol:
                symbol_locs.append(idx)

        line_symbol_locs[line_num] = symbol_locs
    return line_symbol_locs


def step_lat(line: str, idx: int, direction: Literal["left", "right"]) -> int | None:
    op = operator.add if direction == "right" else operator.sub
    num: str = line[idx]
    i: int = op(idx, 1)
    while line[i] != ".":
        num += line[i]
        i = op(i, 1)
        if i < 0 or i > len(line) - 1:
            break
    try:
        for s in ENGLISH_SYMBOLS:
            num = num.strip(s)
        if direction == "left":
            num = num[::-1]
        return int(num.strip("."))
    except ValueError:
        return None


def check_line_vertically(line: str, idx: int) -> list[int]:
    if idx < 0 or idx > len(line) - 1:
        return []

    left_valid: bool = idx - 1 >= 0
    right_valid: bool = idx + 1 <= len(line) - 1
    # 1. If the character is a number:
    if line[idx].isdigit():
        #   a. Check if the character before and after it are dots
        if (left_valid and line[idx - 1] == ".") and (
            right_valid and line[idx + 1] == "."
        ):
            #       b. If they are, add number to a list of numbers to be returned and return the list
            return [int(line[idx])]

        # Start of line and number found
        elif idx == 0 and line[idx].isdigit():
            return [step_lat(line, idx, "right")]

        # End of line and number found
        elif idx == len(line) - 1 and line[idx].isdigit():
            return [step_lat(line, idx, "left")]

        #   c. If both are numbers, return that number (there will be no diagonal numbers in this case)
        elif (left_valid and line[idx - 1].isdigit()) and (
            right_valid and line[idx + 1].isdigit()
        ):
            final_num: str = ""
            # Find the start of the number
            l: int = idx
            while line[l - 1] != ".":
                l -= 1

            # Go from left to right to get the whole number
            r: int = l
            while line[r] != ".":
                final_num += line[r]
                r += 1

            # Remove any symbols that might have gotten caught up in it
            for s in ENGLISH_SYMBOLS:
                final_num.strip(s)
            if not final_num:
                return []
            return [int(final_num)]

        #   d. If one is a number, get the whole number and return it
        elif idx - 1 >= 0 and line[idx - 1] == ".":
            # Get right number
            return [step_lat(line, idx, "right")]

        elif idx + 1 <= len(line) - 1 and line[idx + 1] == ".":
            # Get left number
            return [step_lat(line, idx, "left")]

    # 2. If the character is a dot:
    elif line[idx] == ".":  # or line[idx] in ENGLISH_SYMBOLS:
        ret_list: list[int] = []
        #   a. Move one up and one down the line and check if the character is a number
        if left_valid:
            #   b. If it is, get the whole number and add it to the list of numbers to be returned
            ret_list.append(step_lat(line, idx, "left"))
        if right_valid:
            ret_list.append(step_lat(line, idx, "right"))
        #   c. Return the list
        return ret_list


def get_vertical_values(
    line_num: int, i: int, schematic: list[str], direction: Literal["above", "below"]
) -> list[int]:
    op = operator.add if direction == "below" else operator.sub
    vertical: list[int | None] = check_line_vertically(
        line=schematic[op(line_num, 1)],
        idx=i,
    )
    return vertical


def flatten_list(nested_list):
    flat_list = []
    for element in nested_list:
        if isinstance(element, list):
            flat_list.extend(flatten_list(element))  # Recursively flatten the sublist
        else:
            flat_list.append(element)
    return flat_list


def get_adjacent_part_nums(
    sym_line_idx: int, line_num: int, last_line: int, schematic: list[str]
) -> list[int]:
    ret_list: list[int] = []

    if sym_line_idx != 0:
        left_values: list[int | None] = step_lat(
            schematic[line_num], sym_line_idx, "left"
        )
        ret_list.append(left_values)
    if sym_line_idx != len(schematic[line_num]) - 1:
        right_values: list[int | None] = step_lat(
            schematic[line_num], sym_line_idx, "right"
        )
        ret_list.append(right_values)

    if line_num != 0:
        all_above = get_vertical_values(line_num, sym_line_idx, schematic, "above")
        ret_list.append(all_above)

    if line_num != last_line:
        all_below = get_vertical_values(line_num, sym_line_idx, schematic, "below")
        ret_list.append(all_below)

    return flatten_list(ret_list)


def get_schematic_sum(
    schematic: list[str], symbol_locations: dict[int, list[int]]
) -> list[int]:
    valid_for_sum: list[int] = []
    last_line: int = list(symbol_locations.keys())[-1]

    for line_num, sym_locs in symbol_locations.items():
        for sym_line_idx in sym_locs:
            valid_for_sum.extend(
                get_adjacent_part_nums(sym_line_idx, line_num, last_line, schematic)
            )

    flat_valid_for_sum: list[int | None] = flatten_list(valid_for_sum)
    int_list: list[int] = list(filter(lambda t: isinstance(t, int), flat_valid_for_sum))
    return int_list


def get_gear_ratios(
    schematic: list[str], gear_locations: dict[int, list[int]]
) -> list[int]:
    gear_ratios: list[int] = []
    last_line: int = len(schematic) - 1
    for line_num, gear_locs in gear_locations.items():
        for g_loc in gear_locs:
            adjacent_part_nums: list[int] = get_adjacent_part_nums(
                g_loc, line_num, last_line, schematic
            )
            adjacent_part_nums = list(
                filter(lambda i: i is not None, adjacent_part_nums)
            )
            if len(adjacent_part_nums) == 2:
                gear_ratios.append(adjacent_part_nums[0] * adjacent_part_nums[1])

    return sum(gear_ratios)


if __name__ == "__main__":
    # with open("test_input.txt", "r") as f:
    with open("day3_input.txt", "r") as f:
        schematic = f.readlines()
        schematic = [line.strip() for line in schematic]

    # Part 1
    symbol_locations = get_symbol_indexes(schematic=schematic, symbol=ENGLISH_SYMBOLS)
    ic(sum(get_schematic_sum(schematic, symbol_locations)))

    # Part 2
    gear_locations = get_symbol_indexes(schematic=schematic, symbol="*")
    ic(get_gear_ratios(schematic=schematic, gear_locations=gear_locations))

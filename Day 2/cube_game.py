"""Solution for part A of the Day 2 challenge in Advent of Code 2023."""

import itertools as it

from icecream import ic


def get_possible_game_ids(
    games: dict[str, int], check_maxes: dict[str, int]
) -> list[int]:
    possible_ids: list[int] = []
    for game_id, game_values in games.items():
        game_possible: bool = True
        for color in game_values:
            if game_values[color] > check_maxes[color]:
                game_possible = False
        if game_possible:
            possible_ids.append(game_id)

    return possible_ids


def find_highest_color_count_per_game(game: str) -> dict[str, int]:
    game: list[str] = game.split(":")[1]
    bag_grabs: list[str] = [g.strip() for g in game.split(";")]
    single_color_split: list[str] = it.chain(*[grab.split(",") for grab in bag_grabs])
    single_color_split: list[str] = [n.strip() for n in single_color_split]

    highest_color_counts: dict[str, int] = {"red": 0, "green": 0, "blue": 0}
    for color in ["red", "green", "blue"]:
        all_color: list[str] = [h for h in single_color_split if color in h]
        highest_color_counts[color] = max([int(ac.split(" ")[0]) for ac in all_color])

    return highest_color_counts


def sum_powers_of_min_cube_counts(games: dict[str, int]) -> int:
    all_powers: list[int] = []
    for game_values in games.values():
        power = game_values["red"] * game_values["green"] * game_values["blue"]
        all_powers.append(power)
    return sum(all_powers)


if __name__ == "__main__":
    # Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes.
    # What is the sum of the IDs of those games?

    with open("day2_input.txt", "r") as f:
        data: list[str] = f.readlines()
        data: list[str] = [term.strip() for term in data]

    # test_data = [
    #     "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    #     "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    #     "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    #     "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    #     "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    # ]

    games_with_peak_colors = {}
    for game in data:
        game_id: int = int(game.split(":")[0].split(" ")[1])
        games_with_peak_colors[game_id] = find_highest_color_count_per_game(game)

    check_dict: dict[str, int] = {"red": 12, "green": 13, "blue": 14}
    possible_ids: list[int] = get_possible_game_ids(
        games=games_with_peak_colors, check_maxes=check_dict
    )
    # Answer to part 1
    print(sum(possible_ids))

    # Answer to part 2
    print(sum_powers_of_min_cube_counts(games=games_with_peak_colors))

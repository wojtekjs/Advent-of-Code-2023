"""Solution to part B of Day 1 challenge of the Advent of Code 2023."""

from icecream import ic


# Convert alpha numbers into their numeric equivalents but in string form (e.g., "nine" -> "9").
def convert_alpha_to_numeric(data: list[str]) -> list[int]:
    valid_alpha_numbers = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    data_reworked: list[int] = []
    for term in data:
        term_reworked: str = ""
        running_term: str = ""
        for l in term:
            if l in list(valid_alpha_numbers.values()):
                term_reworked += l
                continue

            running_term += l
            if any(alpha == running_term for alpha in valid_alpha_numbers):
                term_reworked += valid_alpha_numbers.get(running_term)
                running_term = running_term[-1:]
                continue

            while running_term:
                # Covers edge cases like "eightwothree"
                if not any(
                    alpha.startswith(running_term) for alpha in valid_alpha_numbers
                ):
                    running_term = running_term[1:]
                break
        data_reworked.append(int(term_reworked[0] + term_reworked[-1]))

    return data_reworked


if __name__ == "__main__":
    with open("aoc_d1_input.txt", "r") as f:
        data = f.readlines()
        data = [term.strip() for term in data]
    # Test data
    # data = [
    #     "two1nine",
    #     "eightwothree",
    #     "abcone2threexyz",
    #     "xtwone3four",
    #     "4nineeightseven2",
    #     "zoneight234",
    #     "7pqrstsixteen",
    #     # "sevenine",
    #     # "eighthree",
    #     # "oneight",
    # ]
    print(sum(convert_alpha_to_numeric(data)))

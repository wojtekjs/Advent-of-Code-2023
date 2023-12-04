"""Solution to part A of the Day 1 challenge of the Advent of Code 2023."""


# For each term, get the two-digit number contained within by combining the first appearing digit with the last appearing digit.
def get_first_and_last(data: list[str]) -> list[int]:
    two_digits: list[int] = []
    for term in data:
        no_letter_term: list[str] = []
        for l in term:
            try:
                int(l)
            except ValueError:
                continue
            else:
                no_letter_term.append(l)

        two_digit = no_letter_term[0] + no_letter_term[-1]
        two_digits.append(int(two_digit))
    return two_digits


if __name__ == "__main__":
    with open("aoc_d1_input.txt", "r") as f:
        data = f.readlines()
        data = [term.strip() for term in data]

    # Sum all the numbers.
    final_sum = sum(get_first_and_last(data=data))
    print(final_sum)

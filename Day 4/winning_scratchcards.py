from dataclasses import dataclass
from functools import cached_property


@dataclass
class ScratchCard:
    card_num: int
    winning_numbers: list[int]
    card_numbers: list[int]
    card_count: int = 1

    @cached_property
    def matches(self) -> int:
        return len([num for num in self.card_numbers if num in self.winning_numbers])


def calculate_card_points(card: ScratchCard) -> int:
    points: int = 1 if card.matches > 0 else 0
    for _ in range(card.matches - 1):
        points *= 2
    return points


def to_scratch_card(card: str) -> ScratchCard:
    card_num: list[str] = list(card.split(":")[0])
    card_num: int = int("".join([n for n in card_num if n.isdigit()]))

    nums: list[str] = card.split(":")[1]
    win_nums: list[str] = nums.split("|")[0].split(" ")
    card_nums: list[str] = nums.split("|")[1].split(" ")

    win_nums: list[int] = [int(num) for num in win_nums if num != ""]
    card_nums: list[int] = [int(num) for num in card_nums if num != ""]

    return ScratchCard(
        card_num=card_num, winning_numbers=win_nums, card_numbers=card_nums
    )


def find_index_in_list(card_num_needed: int, card_list: list[ScratchCard]) -> int:
    # sourcery skip: use-next
    for i, card in enumerate(card_list):
        if card.card_num == card_num_needed:
            return i
    return None


def spawn_child_cards_Recursive(
    curr_list_idx: int,
    unique_cards: dict[int, ScratchCard],
    card_list: list[ScratchCard],
) -> list[ScratchCard]:
    curr_card: ScratchCard = card_list[curr_list_idx]
    if curr_card == card_list[-1]:
        return card_list

    for m_count in range(1, curr_card.matches + 1):
        insertion_card_num: int = curr_card.card_num + m_count

        card_to_insert: ScratchCard = unique_cards[insertion_card_num]
        insertion_loc: int = find_index_in_list(
            card_num_needed=insertion_card_num, card_list=card_list
        )
        card_list.insert(insertion_loc, card_to_insert)

    return spawn_child_cards_Recursive(
        curr_list_idx=curr_list_idx + 1,
        card_list=card_list,
        unique_cards=unique_cards,
    )


def count_child_cards(
    curr_card_num: int, unique_cards: dict[int, ScratchCard]
) -> dict[int, ScratchCard]:  # sourcery skip: use-itertools-product
    curr_card: ScratchCard = unique_cards.get(curr_card_num)
    if curr_card == unique_cards.get(len(unique_cards) - 1):
        return unique_cards

    for _ in range(1, curr_card.card_count + 1):
        for m_count in range(1, curr_card.matches + 1):
            unique_cards[curr_card_num + m_count].card_count += 1

    return count_child_cards(curr_card_num=curr_card_num + 1, unique_cards=unique_cards)


if __name__ == "__main__":
    # with open("test_input1.txt", "r") as f:
    with open("day4_input.txt", "r") as f:
        cards = f.readlines()
        cards = [card.strip() for card in cards]

    cards: list[ScratchCard] = [to_scratch_card(card) for card in cards]
    all_points: list[int] = [calculate_card_points(card) for card in cards]

    # Part 1
    # print(sum(all_points))

    # Part 2
    unique_cards: dict[int, ScratchCard] = {card.card_num: card for card in cards}

    # all_cards: list[ScratchCard] = spawn_child_cards_Recursive(
    #     curr_list_idx=0, card_list=cards, unique_cards=unique_cards
    # )
    # print(len(all_cards))

    all_cards: dict[int, ScratchCard] = count_child_cards(
        curr_card_num=1, unique_cards=unique_cards
    )
    counts: list[int] = [card.card_count for card in all_cards.values()]
    print(sum(counts))

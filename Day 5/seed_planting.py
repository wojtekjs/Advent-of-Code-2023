from dataclasses import dataclass

import pandas as pd
from icecream import ic


@dataclass
class Range:
    source: int
    destination: int
    length: int


@dataclass
class Map:
    source_name: str
    destination_name: str
    ranges: list[Range]


def get_map_chunks(almanac: list[str]) -> list[list[str]]:
    chunks: list[list[str]] = []
    for i, line in enumerate(almanac[1:], start=1):
        chunk: list[str] = []
        if "map" in line:
            chunk.append(line)
            r: int = i + 1
            while r <= len(almanac) - 1 and "map" not in almanac[r]:
                chunk.append(almanac[r])
                r += 1
        chunks.append(chunk)
    return [chunk for chunk in chunks if chunk != []]


def get_map(map_chunk: list[str]) -> Map:
    conversion: str = map_chunk[0].split(" ")[0].split("-")
    sn, dn = conversion[0], conversion[2]
    range_list: list[Range] = []
    for range_ in map_chunk[1:]:
        range_ = [int(num.strip()) for num in range_.split(" ") if num != ""]
        range_list.append(
            Range(source=range_[1], destination=range_[0], length=range_[2])
        )
    return Map(sn, dn, range_list)


def get_seeds(seed_line: str) -> list[int]:
    seed_nums: list[str] = seed_line.split(":")[1].split(" ")
    return [int(num.strip()) for num in seed_nums if num != ""]


def build_df_from_map_targeted(
    planting_map: Map, target_values: list[int]
) -> pd.DataFrame:
    map_df: pd.DataFrame = pd.DataFrame(
        columns=[planting_map.source_name, planting_map.destination_name],
    )

    located_tar_vals: list[int] = []
    for range_obj in planting_map.ranges:
        for tar_val in target_values:
            if range_obj.source <= tar_val <= range_obj.source + range_obj.length:
                located_tar_vals.append(tar_val)
                diff: int = tar_val - range_obj.source
                corresponding_destination_value: int = range_obj.destination + diff
                map_df.loc[len(map_df)] = [tar_val, corresponding_destination_value]

    for tar_val in target_values:
        if tar_val not in located_tar_vals:
            map_df.loc[len(map_df)] = [tar_val, tar_val]

    return map_df.sort_values(by=planting_map.source_name, ascending=True)


def fuse_dfs(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    starting_df: pd.DataFrame = dfs[0]
    for df in dfs[1:]:
        starting_df = starting_df.merge(df, on=df.columns[0], how="outer")
    return starting_df


def get_lowest_location_number(final_df: pd.DataFrame, seeds: list[int]) -> int:
    return int(
        final_df[final_df["seed"].apply(lambda s: s in seeds)][["location"]]
        .sort_values(by="location", ascending=True)
        .head(1)["location"]
    )


def get_puzzle_response_lowest_loc(almanac: list[str], seeds: list[int]) -> None:
    map_chunks: list[list[str]] = get_map_chunks(almanac)
    maps: list[Map] = [get_map(chunk) for chunk in map_chunks]
    map_dfs: list[pd.DataFrame] = []
    for i, m in enumerate(maps):
        # tar_v is either the seed values for the first DF or the last DF's right most column (which is their overlap/link column)
        tar_v: list[int] = (
            seeds if i == 0 else list(map_dfs[-1][map_dfs[-1].columns[1]])
        )
        map_dfs.append(build_df_from_map_targeted(planting_map=m, target_values=tar_v))

    final_df: pd.DataFrame = fuse_dfs(map_dfs)

    lowest_location: int = get_lowest_location_number(final_df, seeds)
    ic(lowest_location)


def get_seed_ranges(seed_line: str) -> list[int]:
    seed_ints: list[int] = get_seeds(seed_line)
    all_seeds: list[int] = []
    for seed_idx in range(0, len(seed_ints), 2):
        range_start: int = seed_ints[seed_idx]
        range_len: int = seed_ints[seed_idx + 1]
        all_seeds.extend([range_start + i for i in range(range_len)])
    return all_seeds


if __name__ == "__main__":
    # with open("test_input1.txt", "r") as f:
    with open("day5_input.txt", "r") as f:
        almanac = f.readlines()
        almanac = list(filter(lambda l: l != "", [line.strip() for line in almanac]))

    # Part 1: What is the lowest location number that corresponds to any of the initial seed numbers?
    # Seed line is always the first in the almanac
    seeds: list[int] = get_seeds(seed_line=almanac[0])
    get_puzzle_response_lowest_loc(almanac, seeds)

    # Part 2: Same question, but the `seed:` line now represents ranges (num1 is the start point and num2 is the length of the range. E.g., 79 14: range of seeds containing values 79, 80, ... 91, 92.)
    seeds: list[int] = get_seed_ranges(seed_line=almanac[0])
    # TODO Takes an impossibly long time. Need new solution
    get_puzzle_response_lowest_loc(almanac, seeds)

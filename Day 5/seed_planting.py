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


def build_df_from_map(planting_map: Map) -> pd.DataFrame:
    print(f"{planting_map.source_name} -> {planting_map.destination_name}.")
    max_df: int = 0
    for range_obj in planting_map.ranges:
        biggest: int = max(
            range_obj.destination + range_obj.length,
            range_obj.source + range_obj.length,
        )
        if biggest > max_df:
            max_df = biggest
    print(f"Determined {max_df=}.")

    # TODO still getting some NaNs here for some reason
    map_df: pd.DataFrame = pd.DataFrame(
        index=range(1, max_df + 1),
        columns=[planting_map.source_name, planting_map.destination_name],
    )
    print("Populating template DF.")
    for i in range(1, max_df + 1):
        map_df.at[i, planting_map.source_name] = i
        map_df.at[i, planting_map.destination_name] = i

    # This is the clutch code that makes it happen
    for i, range_obj in enumerate(planting_map.ranges):
        print(f"Parsing Range {i}/{len(planting_map.ranges)}")
        for c in range(range_obj.length):
            map_df.at[range_obj.source + c, planting_map.destination_name] = (
                range_obj.destination + c
            )

    return map_df.sort_values(by=planting_map.source_name, ascending=True)


def fuse_dfs(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    starting_df: pd.DataFrame = dfs[0]
    for df in dfs[1:]:
        starting_df = starting_df.merge(df, on=df.columns[0], how="outer")
    return starting_df


def get_lowest_location_number(final_df: pd.DataFrame) -> int:
    return int(
        final_df[final_df["seed"].apply(lambda s: s in seeds)][["location"]]
        .sort_values(by="location", ascending=True)
        .head(1)["location"]
    )


# NOTE there is an optimisation here where I just parse the calc for seeds and matching lines??
if __name__ == "__main__":
    # with open("test_input1.txt", "r") as f:
    with open("day5_input.txt", "r") as f:
        almanac = f.readlines()
        almanac = list(filter(lambda l: l != "", [line.strip() for line in almanac]))

    # Seed line is always the first in the almanac
    seeds = get_seeds(seed_line=almanac[0])
    ic()
    map_chunks: list[list[str]] = get_map_chunks(almanac)
    ic()
    maps: list[Map] = [get_map(chunk) for chunk in map_chunks]
    ic()
    map_dfs: list[pd.DataFrame] = [
        build_df_from_map(planting_map) for planting_map in maps
    ]
    ic()
    final_df: pd.DataFrame = fuse_dfs(map_dfs)
    ic()

    # Part 1: What is the lowest location number that corresponds to any of the initial seed numbers?
    lowest_location: int = get_lowest_location_number(final_df)
    ic(lowest_location)

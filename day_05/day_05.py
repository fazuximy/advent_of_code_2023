# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 18:34:42 2023

@author: Fazuximy
"""

import os
from dataclasses import dataclass, field
import numpy as np
import re

from utils.utils import import_txt_as_chunks



# Part 1

"""
The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51

With this map, you can look up the soil number required for each initial seed number:

    Seed number 79 corresponds to soil number 81.
    Seed number 14 corresponds to soil number 14.
    Seed number 55 corresponds to soil number 57.
    Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

    Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
    Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.

So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?
"""


@dataclass
class ConversionData:
    seeds:list[int]
    soil:list[int] = field(default_factory=list)
    fertilizer:list[int] = field(default_factory=list)
    water:list[int] = field(default_factory=list)
    light:list[int] = field(default_factory=list)
    temperature:list[int] = field(default_factory=list)
    humidity:list[int] = field(default_factory=list)
    locations:list[int] = field(default_factory=list)

@dataclass
class MappingData:
    mapping_type:str
    source_start:int
    destination_start:int
    mapping_range:int


@dataclass
class AlmanacData:
    seed_to_soil: list[MappingData] = field(default_factory=list)
    soil_to_fertilizer: list[MappingData] = field(default_factory=list)
    fertilizer_to_water: list[MappingData] = field(default_factory=list)
    water_to_light: list[MappingData] = field(default_factory=list)
    light_to_temperature: list[MappingData] = field(default_factory=list)
    temperature_to_humidity: list[MappingData] = field(default_factory=list)
    humidity_to_location: list[MappingData] = field(default_factory=list)

def mapping(source_data:int,MappingDataObjects:list[MappingData]):
    
    for MappingDataObject in MappingDataObjects:
        
        source_start = MappingDataObject.source_start
        source_end = source_start + MappingDataObject.mapping_range
        destination_start = MappingDataObject.destination_start
        
        if source_start <= source_data < source_end:
            
            source_delta = source_data - source_start
            
            destination_data = destination_start + source_delta
            
            break
            
        else:
            destination_data = source_start
    
    
    return destination_data



working_directory = os.getcwd()

data_filename = "input.xscore"

input_file_directory = os.path.join(working_directory,"data",data_filename)

txt_chunks = import_txt_as_chunks(input_file_directory)

seeds = [int(seed) for seed in re.findall("\d+",txt_chunks[0])]

ConvertedData = ConversionData(seeds)

AlmanacMappingData = AlmanacData()

for mapping_information in txt_chunks[1:]:
    
    mapping_lines = mapping_information.splitlines()
    
    mapping_name = mapping_lines[0].split(" ")[0]
    mapping_name = re.sub("\-","_",mapping_name)
    
    mappings = []
    for mapping_line in mapping_lines[1:]:
    
        mapping_information = re.findall("\d+",mapping_line)
    
        source_start = int(mapping_information[1])
        destination_start = int(mapping_information[0])
        mapping_range = int(mapping_information[2])
        mappings.append(MappingData(mapping_name, source_start, destination_start, mapping_range))
       
    AlmanacMappingData.__dict__[mapping_name] = mappings


ConvertedData.soil = [mapping(seed,AlmanacMappingData.seed_to_soil) for seed in ConvertedData.seeds]

ConvertedData.fertilizer = [mapping(soil,AlmanacMappingData.soil_to_fertilizer) for soil in ConvertedData.soil]

ConvertedData.water = [mapping(fertilizer,AlmanacMappingData.fertilizer_to_water) for fertilizer in ConvertedData.fertilizer]

ConvertedData.light = [mapping(water,AlmanacMappingData.water_to_light) for water in ConvertedData.water]

ConvertedData.temperature = [mapping(light,AlmanacMappingData.light_to_temperature) for light in ConvertedData.light]

ConvertedData.humidity = [mapping(temperature,AlmanacMappingData.temperature_to_humidity) for temperature in ConvertedData.temperature]

ConvertedData.locations = [mapping(humidity,AlmanacMappingData.humidity_to_location) for humidity in ConvertedData.humidity]

print("The lowest location number that corresponds to any of the initial seed numbers is: {}".format(np.min(ConvertedData.locations)))



# Part 2

"""
The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13

This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
"""


seed_range = []
for seed_numb in range(0,len(seeds),2):
    
    start_seed = seeds[seed_numb]
    seed_numbers = seeds[seed_numb+1]
    end_seed = start_seed+seed_numbers
    
    seed_range.append([start_seed, end_seed])


NewSeedsConvertedData = ConversionData(new_seeds)


np.min(NewSeedsConvertedData.locations)


def split_range_mapping(source_range:list[list[int]],MappingDataObjects:list[MappingData]):
    
    for MappingDataObject in MappingDataObjects:
        
        source_range_start = source_range[0]
        source_range_end = source_range[1]
        source_range_delta = source_range_end - source_range_start
        
        map_source_start = MappingDataObject.source_start
        map_source_end = map_source_start + MappingDataObject.mapping_range
        map_destination_start = MappingDataObject.destination_start
        
        map_and_range_start_delta = map_source_start - source_range_start 
        
        
        
        if map_source_start <= source_range_start < map_source_end:
            
            if map_source_start <= source_range_end < map_source_end:
        
                   
                start_destination_range = map_destination_start + map_and_range_start_delta

                end_destination_range = start_destination_range + source_range_delta
                
                destination_range = [start_destination_range,end_destination_range]
            
                break
            
            else:
            
            
        else:
            destination_data = source_start
    
    
    return destination_data



# TODO Make functions that can split range

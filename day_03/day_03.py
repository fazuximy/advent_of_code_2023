# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 11:54:12 2023

@author: Fazuximy
"""

import os
from dataclasses import dataclass
import numpy as np
import networkx

from utils.utils import import_txt_as_lines

# Part 1

"""
The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""

@dataclass
class NeighborData:
    node:tuple[int]
    neighbors:list[tuple[int]]
    
    
@dataclass
class NumberData:
    number:int
    number_nodes:list[tuple[int]]
    neighbor_nodes: list[tuple[int]]
    special_character: bool
    special_characters: list[str]
    gear:int
    gear_nodes:list[tuple[int]]
    
def recursive_graph_number_extracter(node:tuple[int],graph:networkx.Graph, column_length:int) -> (list[tuple[int]], list[int]):
    
    number_nodes = node
    numbers = graph.nodes(data=True)[node]["attr"]["character"]
    
    new_column_value = node[1] + 1
    
    if new_column_value < column_length:
    
        node_to_right = (node[0],new_column_value)
        
        graph_node = graph.nodes(data=True)[node_to_right]
    
        if graph_node["attr"]["numeric"] == True:
            
            yield number_nodes,numbers
            
            yield from recursive_graph_number_extracter(node_to_right,graph,column_length)
                                                        
        else:
            yield number_nodes,numbers
            
    else:
        yield number_nodes,numbers
            
        

    
def get_number_information(number_nodes:list[tuple[int]],numbers:list[int],graph:networkx.Graph) -> NumberData:
    
    number = int("".join(numbers))
    
    neighbors = []
    
    for number_node in number_nodes:
        
        number_neighbors = graph.neighbors(number_node)
        
        no_numb_neighbor = [neighbor for neighbor in number_neighbors if neighbor not in number_nodes]
        
        neighbors.extend(no_numb_neighbor)
        
        
    special_character = False
    special_characters = []
    gear = False
    gear_nodes = []
    for neighbor in neighbors:
        neighbor_data = graph.nodes(data=True)[neighbor]["attr"]
        special_character = neighbor_data["special_character"]
        if neighbor_data["special_character"] == True:
            special_character = True
            special_characters.append(neighbor_data["character"])
            if neighbor_data["character"] == "*":
                gear = True
                gear_nodes.append(neighbor)
            
    gear_nodes = list(set(gear_nodes))
    NumberDataObject = NumberData(number,number_nodes,neighbors,special_character,special_characters,gear,gear_nodes)
            
    return NumberDataObject 
    


working_directory = os.getcwd()

data_filename = "input.xscore"

input_file_directory = os.path.join(working_directory,"data",data_filename)

engine_lines = import_txt_as_lines(input_file_directory)

engine_points = []
for engine_line in engine_lines:
    engine_points.append(list(engine_line))
    
engine_array = np.array(engine_points)

row_length = engine_array.shape[0]
column_length = engine_array.shape[1]

engine_graph = networkx.Graph()
neighbor_data = []
for row_numb,row in enumerate(engine_array):
    for column_numb,point in enumerate(row):
    
        neighbors = []    
    
        special_character = point.isnumeric() == False and point != "."
        
        engine_graph.add_node((row_numb, column_numb),attr = {"character":str(point), "numeric": point.isnumeric(), "special_character":special_character})
           
        
        left_numb = row_numb-1
        right_numb = row_numb+1
        top_numb = column_numb-1
        bottom_numb = column_numb+1
        
        if top_numb >= 0:
            neighbors.append((row_numb,top_numb))
            
            if left_numb >= 0:
                neighbors.append((left_numb,top_numb))
                
            if right_numb < row_length:
                neighbors.append((right_numb,top_numb))
                
        if bottom_numb < column_length:
            neighbors.append((row_numb,bottom_numb))
            
            if left_numb >= 0:
                neighbors.append((left_numb,bottom_numb))
                
            if right_numb < row_length:
                neighbors.append((right_numb,bottom_numb))
        
        if left_numb >= 0:
            neighbors.append((left_numb,column_numb))
        if right_numb < row_length:
            neighbors.append((right_numb,column_numb))

        neighbor_data.append(NeighborData((row_numb, column_numb), neighbors))
        
        
for neighbors in neighbor_data:
    for neighbor in neighbors.neighbors:
        engine_graph.add_edge(neighbors.node,  neighbor)


number_nodes = []
number_data = []
for node in engine_graph.nodes(data = True):
    
    if node[1]["attr"]["numeric"] == True:

        if node[0] not in number_nodes:

            current_number_nodes, current_numbers = zip(*list(recursive_graph_number_extracter(node[0],engine_graph,column_length)))
            
            number_nodes.extend(current_number_nodes)
            
            number_data.append(get_number_information(current_number_nodes, current_numbers,engine_graph))
        
        
sum_of_part_numbers = sum([data.number for data in number_data if data.special_character == True])


print("The sum of all of the part numbers in the engine schematic is: {}".format(sum_of_part_numbers))


# Part 2

"""
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""

gear_numbers = []
gear_nodes = []

gear_dict = {}
for data in number_data:
    
    if data.gear == True:
        
        for gear_node in data.gear_nodes:
            gear_node = str(gear_node)
            
            if gear_node in gear_dict.keys():
                number = gear_dict[gear_node]
                gear_dict[gear_node] = number+[data.number]
                
            else:
                gear_dict[gear_node] = [data.number]
                
            

gear_ratios = [np.prod(numbers) for numbers in gear_dict.values() if len(numbers) == 2]

print("The sum of all of the gear ratios in your engine schematic is: {}".format(sum(gear_ratios)))


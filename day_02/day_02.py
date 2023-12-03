# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 12:09:15 2023

@author: Fazuximy
"""


import os
from dataclasses import dataclass
import re
import numpy as np

from utils.utils import import_txt_as_lines


# Part 1
"""
You play several games and record the information from each game (your puzzle input). Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

In game 1, three sets of cubes are revealed from the bag (and then put back again). The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?

"""

@dataclass
class RevealData:
    blue_numb: int = 0
    red_numb: int = 0
    green_numb: int = 0


@dataclass
class GameData:
    game_number: int
    reveals: list[RevealData]
    max_blue: int = None
    max_red:int = None
    max_green:int = None
    possible: bool = False
    
    def get_max_for_each_color(self):
        
        blues = []
        reds = []
        greens = []
        
        for reveal in self.reveals:
            
            blues.append(reveal.blue_numb)
            reds.append(reveal.red_numb)
            greens.append(reveal.green_numb)
            
        self.max_blue = max(blues)
        self.max_red = max(reds)
        self.max_green = max(greens)
            


@dataclass
class Rules():
    max_blue: int
    max_red: int
    max_green: int


def check_if_possible(GameDataObject:GameData, RuleObejct:Rules):
    
    blue_possible = GameDataObject.max_blue <= RuleObejct.max_blue
    
    red_possible = GameDataObject.max_red <= RuleObejct.max_red
    
    green_possible = GameDataObject.max_green <= RuleObejct.max_green
    
    GameDataObject.possible = all([blue_possible,red_possible,green_possible])
    

working_directory = os.getcwd()

data_filename = "input.xscore"

input_file_directory = os.path.join(working_directory,"day_02","data",data_filename)

game_lines = import_txt_as_lines(input_file_directory)

MaxColorsAllowed = Rules(max_blue=14,max_red=12,max_green=13)

games = []
for game_line in game_lines:
    
    game_name, game = game_line.split(":")
    
    game_number = int(re.findall("\d+", game_name)[0])
    
    game_reveals = game.split(";")
    
    reveal_data = []
    
    for game_reveal in game_reveals:
        
        color_reveals = game_reveal.split(",")
        
        colors = [re.findall("[a-zA-Z]+",color_reveal)[0] for color_reveal in color_reveals]
        numbers = [int(re.findall("\d+",color_reveal)[0]) for color_reveal in color_reveals]
        
        RevealDataObject = RevealData()
        
        for color,number in zip(colors,numbers):
            
            if color == "blue":
                RevealDataObject.blue_numb = number
                
            elif color == "red":
                RevealDataObject.red_numb = number
                
            elif color == "green":
                RevealDataObject.green_numb = number
                
        reveal_data.append(RevealDataObject)
               
    GameDataObject = GameData(game_number,reveal_data)
        
    GameDataObject.get_max_for_each_color()
    
    check_if_possible(GameDataObject,MaxColorsAllowed)
    
    games.append(GameDataObject)
        
        
possible_game_numbers = [game.game_number for game in games if game.possible]
    
print("The sum of possible game ids is: {}".format(sum(possible_game_numbers)))
    


# Part 2
"""
As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

    In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
    Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
    Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
    Game 4 required at least 14 red, 3 green, and 15 blue cubes.
    Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.

The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
"""


min_colors_multiplied = [np.prod([game.max_blue,game.max_red,game.max_green]) for game in games]

print("The product of the fewest number of cubes for all the games is: {}".format(sum(min_colors_multiplied)))


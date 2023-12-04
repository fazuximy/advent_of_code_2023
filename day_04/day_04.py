# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 17:50:42 2023

@author: Fazuximy
"""

import os
from dataclasses import dataclass
import numpy as np
import re

from utils.utils import import_txt_as_lines


# Part 1
"""
The Elf leads you over to the pile of colorful cards. There, you discover dozens of scratchcards, all with their opaque covering already scratched off. Picking one up, it looks like each card has two lists of numbers separated by a vertical bar (|): a list of winning numbers and then a list of numbers you have. You organize the information into a table (your puzzle input).

As far as the Elf has been able to figure out, you have to figure out which of the numbers you have appear in the list of winning numbers. The first match makes the card worth one point and each match after the first doubles the point value of that card.

For example:

Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11

In the above example, card 1 has five winning numbers (41, 48, 83, 86, and 17) and eight numbers you have (83, 86, 6, 31, 17, 9, 48, and 53). Of the numbers you have, four of them (48, 83, 17, and 86) are winning numbers! That means card 1 is worth 8 points (1 for the first match, then doubled three times for each of the three matches after the first).

    Card 2 has two winning numbers (32 and 61), so it is worth 2 points.
    Card 3 has two winning numbers (1 and 21), so it is worth 2 points.
    Card 4 has one winning number (84), so it is worth 1 point.
    Card 5 has no winning numbers, so it is worth no points.
    Card 6 has no winning numbers, so it is worth no points.

So, in this example, the Elf's pile of scratchcards is worth 13 points.

Take a seat in the large pile of colorful cards. How many points are they worth in total?
"""

@dataclass
class CardData:
    card_number:int
    own_numbers: list[int]
    winning_numbers: list[int]
    matching_winning_numbers: list[int] = None
    points: int = None


def get_matching_winning_numbers(CardDataObject: CardData):
    
    matching_numbers = [number for number in CardDataObject.own_numbers if number in CardDataObject.winning_numbers]
    
    CardDataObject.matching_winning_numbers = matching_numbers
    

def _calculate_points(matching_numbers:list[int]):
    
    number_of_matching = len(matching_numbers)
    
    if number_of_matching  > 0:
        points = 2**(number_of_matching-1) 
    else:
        points = 0
    
    return points

def get_points(CardDataObject: CardData):
    
    points = _calculate_points(CardDataObject.matching_winning_numbers)
    
    CardDataObject.points = points


working_directory = os.getcwd()

data_filename = "input.xscore"

input_file_directory = os.path.join(working_directory,"data",data_filename)

card_lines = import_txt_as_lines(input_file_directory)

"""
test_data = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n\
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\n\
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\n\
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\n\
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\n\
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"

card_lines = test_data.splitlines()
"""

card_data_objects = []
for card_line in card_lines:
    
    card_name, card_numbers = card_line.split(":")
    card_name_number = int(re.findall("\d+", card_name)[0])
    
    own_numbers, winning_numbers = card_numbers.split("|")
    
    own_numbers_clean = [int(number) for number in re.findall("\d+",own_numbers)]
    winning_numbers_clean = [int(number) for number in re.findall("\d+",winning_numbers)]
    
    card_data_objects.append(CardData(card_name_number,own_numbers_clean,winning_numbers_clean))
                         

[get_matching_winning_numbers(CardData) for CardData in card_data_objects]

[get_points(CardData) for CardData in card_data_objects]


card_points = [CardData.points for CardData in card_data_objects]

print("The total number of points is: {}".format(sum(card_points)))



"""
Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.

Copies of scratchcards are scored like normal scratchcards and have the same card number as the card they copied. So, if you win a copy of card 10 and it has 5 matching numbers, it would then win a copy of the same cards that the original card 10 won: cards 11, 12, 13, 14, and 15. This process repeats until none of the copies cause you to win any more cards. (Cards will never make you copy a card past the end of the table.)

This time, the above example goes differently:

Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11

    Card 1 has four matching numbers, so you win one copy each of the next four cards: cards 2, 3, 4, and 5.
    Your original card 2 has two matching numbers, so you win one copy each of cards 3 and 4.
    Your copy of card 2 also wins one copy each of cards 3 and 4.
    Your four instances of card 3 (one original and three copies) have two matching numbers, so you win four copies each of cards 4 and 5.
    Your eight instances of card 4 (one original and seven copies) have one matching number, so you win eight copies of card 5.
    Your fourteen instances of card 5 (one original and thirteen copies) have no matching numbers and win no more cards.
    Your one instance of card 6 (one original) has no matching numbers and wins no more cards.

Once all of the originals and copies have been processed, you end up with 1 instance of card 1, 2 instances of card 2, 4 instances of card 3, 8 instances of card 4, 14 instances of card 5, and 1 instance of card 6. In total, this example pile of scratchcards causes you to ultimately have 30 scratchcards!

Process all of the original and copied scratchcards until no more scratchcards are won. Including the original set of scratchcards, how many total scratchcards do you end up with?
"""





card_data_objects[-2].points


card_results = []
for CardData in card_data_objects:
    
    if CardData.points > 0:
        card_start = CardData.card_number+1
        card_end = card_start+len(CardData.matching_winning_numbers)
        
        card_results.append(list(range(card_start,card_end)))
        
    else:
        card_results.append([])

card_numbers = [CardData.card_number for CardData in card_data_objects]

card_result_dict = dict(zip(card_numbers,card_results))
    
total_cards_dict = dict(zip(card_numbers,[1]*len(card_numbers)))

new_cards_dict = dict(zip(card_numbers,[1]*len(card_numbers)))


def recursive_scratchcards(current_cards_dict, card_result_dict, total_cards_dict):
    
    new_cards_dict = dict(zip(current_cards_dict.keys(),[0]*len(current_cards_dict.keys())))
    
    for card_numb in current_cards_dict.keys():
        
        number_of_cards = current_cards_dict[card_numb]
        
        for new_card_numb in card_result_dict[card_numb]:
            
            new_cards_dict[new_card_numb] = new_cards_dict[new_card_numb] + number_of_cards
            total_cards_dict[new_card_numb] = total_cards_dict[new_card_numb] + number_of_cards
    
    if sum(new_cards_dict.values()) == 0:
        return total_cards_dict        
    else:
        return recursive_scratchcards(new_cards_dict,card_result_dict,total_cards_dict)

    
    
total_number_of_cards_dict = recursive_scratchcards(new_cards_dict, card_result_dict,total_cards_dict)

    
print("The total number of scratchcards is: {}".format(sum(total_number_of_cards_dict.values())))

    
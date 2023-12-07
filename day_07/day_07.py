# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 21:00:44 2023

@author: Fazuximy
"""


import os
from dataclasses import dataclass
import numpy as np

from utils.utils import import_txt_as_lines

import pandas as pd


"""
In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards' labels are distinct: 23456

Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

    32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
    KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
    T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.

Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?
"""


@dataclass
class HandData:
    string_hand:str
    cards_in_hand:list[str]
    bid:int
    hand_type: str
    hand_type_rank:int
    card_ranks:list[int]
    
    
def determine_card_type(hand_count: pd.Series) -> str:
    
    hand_count_values = list(hand_count.values)
    
    if 5 in hand_count_values:
        
        hand_type = "five_of_a_kind"
        
    elif 4 in hand_count_values:
        
        hand_type = "four_of_a_kind"
        
    elif 3 in hand_count_values:
        
        if 2 in hand_count_values:
        
            hand_type = "full_house"
            
        else:
            
            hand_type = "three_of_a_kind"
            
    elif 2 in hand_count_values:
        
        if hand_count_values.count(2) == 2:
            
            hand_type = "two_pairs"
            
        else:
            
            hand_type = "one_pair"
            
    else:
        
        hand_type = "high_card"
        
    return hand_type


working_directory = os.getcwd()

data_filename = "input.xscore"

input_file_directory = os.path.join(working_directory,"data",data_filename)

hand_lines = import_txt_as_lines(input_file_directory)

# lower is better 
type_point_dict = {"five_of_a_kind":1,"four_of_a_kind":2, "full_house":3, "three_of_a_kind":4, "two_pairs":5, "one_pair":6, "high_card":7}
cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
card_point_dict = dict(zip(cards,list(range(1,len(cards)+1))))


hands = []

for hand_line in hand_lines:
    hand, bid = hand_line.split(" ")
    
    bid = int(bid)
    
    hand_cards = list(hand)
    
    card_ranks = [card_point_dict[card] for card in hand_cards]
    
    hand_count = pd.Series(hand_cards).value_counts()
    
    hand_type = determine_card_type(hand_count)
    
    hand_type_rank = type_point_dict[hand_type]
    
    hands.append(HandData(hand,hand_cards,bid,hand_type,hand_type_rank,card_ranks))
    
    
bids = []
hand_type_ranks = []
card_ranks = []
for hand in hands:
    
    hand_type_ranks.append(hand.hand_type_rank)
    bids.append(hand.bid)
    card_ranks.append(hand.card_ranks)


df_part1 = pd.DataFrame({"hand_type_rank":hand_type_ranks,"bid":bids})
    
df_part2 = pd.DataFrame(card_ranks,columns=['card1','card2','card3','card4','card5'])

result_df = pd.concat([df_part1,df_part2.reindex(df_part1.index)],axis=1)

sorted_result_df = result_df.sort_values(by = ["hand_type_rank",'card1','card2','card3','card4','card5'], ascending = False)

sorted_result_df["sorting_values"] = range(1,len(sorted_result_df["hand_type_rank"])+1)

sorted_result_df["winnings"] = sorted_result_df.sorting_values*sorted_result_df.bid

total_winnings = sum(sorted_result_df["winnings"])

print("The number of total winnings is: {}".format(total_winnings))


# Part 2

"""
To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

    32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
    KK677 is now the only two pair, making it the second-weakest hand.
    T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.

With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
"""


# Brute force could be a solution, just check all possible swap outs for J
    # There are only 1000 data points
    # Even with multiple Js, the best solution would be that they are both the same value


@dataclass
class JokerHandData:
    string_hand:str
    cards_in_hand:list[str]
    bid:int
    hand_type: str
    hand_type_rank:int
    card_ranks:list[int]
    number_of_jokers:int


new_cards = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
new_card_point_dict = dict(zip(new_cards,list(range(1,len(new_cards)+1))))



joker_hands = []

for hand_line in hand_lines:
    hand, bid = hand_line.split(" ")
    
    bid = int(bid)
    
    hand_cards = list(hand)
    
    card_ranks = [new_card_point_dict[card] for card in hand_cards]
    
    hand_count = pd.Series(hand_cards).value_counts()
    
    number_of_jokers = 0
    if "J" in list(hand_count.index):
        number_of_jokers = hand_count["J"]
    
    if number_of_jokers > 0:
        multi_hand_types = []
        multi_hand_type_ranks = []
        for new_card in new_cards[:-1]:
            new_hand_cards = [hand_card if hand_card != "J" else new_card for hand_card in hand_cards]
            new_hand_count = pd.Series(new_hand_cards).value_counts()
            hand_type = determine_card_type(new_hand_count)
            multi_hand_types.append(hand_type)
            multi_hand_type_ranks.append(type_point_dict[hand_type])
            
        hand_type = multi_hand_types[np.argmin(multi_hand_type_ranks)]
                
    else:
        hand_type = determine_card_type(hand_count)
    
    hand_type_rank = type_point_dict[hand_type]
    
    joker_hands.append(JokerHandData(hand,hand_cards,bid,hand_type,hand_type_rank,card_ranks,number_of_jokers))

    
bids = []
hand_type_ranks = []
jokers = []
card_ranks = []
for joker_hand in joker_hands:
    
    hand_type_ranks.append(joker_hand.hand_type_rank)
    bids.append(joker_hand.bid)
    jokers.append(joker_hand.number_of_jokers)
    card_ranks.append(joker_hand.card_ranks)


df_part1 = pd.DataFrame({"hand_type_rank":hand_type_ranks,"bid":bids, "number_of_jokers":jokers})
    
df_part2 = pd.DataFrame(card_ranks,columns=['card1','card2','card3','card4','card5'])

result_df = pd.concat([df_part1,df_part2.reindex(df_part1.index)],axis=1)

sorted_result_df = result_df.sort_values(by = ["hand_type_rank",'card1','card2','card3','card4','card5'], ascending = False)

sorted_result_df["sorting_values"] = range(1,len(sorted_result_df["hand_type_rank"])+1)

sorted_result_df["winnings"] = sorted_result_df.sorting_values*sorted_result_df.bid

total_winnings = sum(sorted_result_df["winnings"])

print("With jokers, the number of total winnings is: {}".format(total_winnings))


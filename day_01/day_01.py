# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 16:31:04 2023

@author: Fazuximy
"""



import os
from dataclasses import dataclass
import regex
import re
import pandas as pd


### PART 1

"""
The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

"""


@dataclass
class CalibrationData:
    numbers:list
    calibration_number: int = None
    
def calculate_calibration_number(CalibrationDataObject: CalibrationData):
    
    numbers = CalibrationDataObject.numbers
    
    calibration_number = int(numbers[0]+numbers[-1])
    
    CalibrationDataObject.calibration_number = calibration_number


working_directory = os.getcwd()

data_filename = "input.xscore"

input_file_directory = os.path.join(working_directory,"data",data_filename)

with open(input_file_directory, 'r') as file:
    calibration_document = file.read()
    
calibration_lines = calibration_document.splitlines()

calibration_numbers = []
for calibration_line in calibration_lines:
    
    CalibrationDataObject = CalibrationData(re.findall("\d",calibration_line))
    
    calculate_calibration_number(CalibrationDataObject)
        
    calibration_numbers.append(CalibrationDataObject.calibration_number)
    
print("Part 1 - The sum of the calibration values are: {}".format(sum(calibration_numbers)))
    
    
    

### Part 2

"""
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
"""

# Task is not properly explained. All matches should be replaced, even though they are overlapping


def _replace_matches(string:str,match_replacements:list[str],match_spans:list[tuple[int]]):
    
    # Replace matches with match replacements in string
    
    string_start = 0
    new_string = ""
    for span, replacement in zip(match_spans, match_replacements):
        new_string = new_string + string[string_start:(span[0])] + replacement
        string_start = span[1]
        
    new_string = new_string + string[span[1]:]
    
    return new_string

def convert_string_patterns_to_corresponding_strings(strings: list[str], pattern_converter:dict) -> list[str]:
    
    converted_strings = []
    for string in strings:
    
        # Getting all matches from dictionary keys
        pattern = '|'.join(pattern_converter.keys())
        matches = regex.finditer(pattern, string, overlapped = True)
            
        # Get the match and span of that dictionary
        match_temp_results = [(match.group(),match.span()) for match in matches]
            
        if len(match_temp_results) > 0:
            
            match_results, match_spans = zip(*match_temp_results)
            match_replacements = [pattern_converter[result] for result in match_results]

            converted_string = _replace_matches(string,match_replacements,match_spans)
                
            converted_strings.append(converted_string)
        else:
            converted_strings.append(string)
            

    return converted_strings
  
# Test dataset  
"""
calibration_lines = ["two1nine",
"eightwothree",
"abcone2threexyz",
"xtwone3four",
"4nineeightseven2",
"zoneight234",
"7pqrstsixteen",
"eighthree",
"sevenine",
"onetwoone"] 
"""

word_digits  = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
number_digits = ["1","2","3","4","5","6","7","8","9"]
digit_dict = dict(zip(word_digits,number_digits))

converted_calibration_lines = convert_string_patterns_to_corresponding_strings(calibration_lines, digit_dict)

corrected_calibration_numbers = []
for converted_calibration_line in converted_calibration_lines:
    
    CorrectedCalibrationData = CalibrationData(re.findall("\d",converted_calibration_line))
    
    calculate_calibration_number(CorrectedCalibrationData)
        
    corrected_calibration_numbers.append(CorrectedCalibrationData.calibration_number)
    
print("Part 2 - The sum of the corrected calibration values are: {}".format(sum(corrected_calibration_numbers)))
    

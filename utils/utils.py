# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 12:10:17 2023

@author: Fazuximy
"""

def import_txt_as_lines(input_file_directory:str) -> list[str]:

    with open(input_file_directory, 'r') as file:
        input_file = file.read()
        
    input_file_lines = input_file.splitlines()
    
    return input_file_lines
    
    
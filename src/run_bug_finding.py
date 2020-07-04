from typing import List, Dict, Union, DefaultDict
from pathlib import Path
import torch  # -> version --> 1.5.0
import numpy as np
import os
import fasttext
from collections import defaultdict
import json
import codecs
from bug_finder import find_bugs


def all_if_as_bugs(json_file):

    data = read_json_file(json_file)
    raw_code = data['raw_source_code']
    split_rawcode = raw_code.split("\n")
    ifcase_linenumber = []
    print(json_file)
    for i,line in enumerate(split_rawcode):
        if ('if (' in line) or ('if(' in line):
            ifcase_linenumber.append(i+1)
    return ifcase_linenumber
    
def find_bugs_in_js_files(list_of_json_file_paths: List[str], token_embedding: fasttext.FastText) -> Dict[str, List[int]]:
    r"""
    Please DO NOT delete the 'metadata' file in the current directory else your submission will not be scored on codalab.

    :param list_of_json_file_paths:
        Example:
            list_of_json_file_paths = [
                'dataset/1.json',
                'dataset/2.json',
                'dataset/3.json',
                'dataset/4.json',
            ]
    :param token_embedding: get embedding for tokens. The pre-trained embeddings have been learned using fastText (https://fasttext.cc/docs/en/support.html)
        Example:
            token_embedding['foo'] # Gets vector representation for the Identifier 'foo'
            token_embedding['true'] # Gets vector representation for the 'true
    :return: A dictionary of the found bugs in the given list of JSON files. The keys should be the file paths and the corresponding values should be list of line numbers where the bug occurs. The format of the dict should be returned as follows:
            {
                'dataset/1.json': [1, 2],
                'dataset/2.json': [11],
                'dataset/3.json': [6],
                'dataset/4.json': [4, 2]
            }
    """

    #####################################################
    #                                                   #
    #   1. Write your code below.                       #
    #   2. You may use the read_json_file() helper      #
    #      function to read a JSON file.                #
    #   3. Return a dict with the found bugs from here. #
    #                                                   #
    #####################################################

    # For each file, the current naive implementation returns a random line number between 1-500
    # Replace this with your own code
    predicted_results = defaultdict(list)

    for fp in list_of_json_file_paths:
        bug_list = find_bugs(fp)
        
        if len(bug_list):
            for i in bug_list:
                predicted_results[fp].append(i)
        else:
            predicted_results[fp] = []
            
    return dict(predicted_results)

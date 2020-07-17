from typing import List, Dict, Union, DefaultDict
from pathlib import Path
import torch  # -> version --> 1.5.0
import numpy as np
import os
import fasttext
from collections import defaultdict
import json
import codecs
import get_token_from_AST
import model
from torch.nn.utils.rnn import pack_padded_sequence, pad_sequence

# Enable Training of the model or just predict solution for a given file
TRAIN_START = False
MAX_LEN = 35
BUG_THRESHOLD = 0.7
    
def find_bugs_in_js_files(list_of_json_file_paths: List[str], token_embedding: fasttext.FastText) -> Dict[str, List[int]]:
    """
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


    if TRAIN_START:
        # Generate tokens and train the model
        model.train_model(list_of_json_file_paths, token_embedding, MAX_LEN)
        return None
    else: # Load the existing model to predict results
        predicted_results = defaultdict(list)

        # use pytorch load method to load the model
        frozen_model = model.load_model("trained_model.pt")
        frozen_model.eval()
        
        # iterate through all the files
        for fp in list_of_json_file_paths:
            # generate tokens from the AST tree for all if conditionals . FALSE indicate disabling of Negative(BUG) tokens
            token_list, token_label, line_list,__,_  = get_token_from_AST.get_token(fp, False)
            
            bug_list = []
            fasttext_token = []

            if len(token_list):
                
                # Trim token list to the maximum length. if token list length is less than the maximum length, add padding "_PAD"
                for line in token_list:                    
                    if len(line) >= MAX_LEN:
                        line = line[0:MAX_LEN]

                    else:
                        while len(line) < MAX_LEN:
                          line.append("_PAD")                    

                    
                    linetoken = []
                    for token in line:
                        linetoken.append(token_embedding[token])
                    fasttext_token.append(torch.tensor(linetoken))

                padded = pad_sequence(fasttext_token, batch_first=True)
                
                #predict results from the trained model
                pred_y = frozen_model(padded)
                pred_tensor = torch.squeeze(pred_y,dim=1)
                
                # if prediciton result is greater than threshold, consider the if condition as bug.
                for i, y in enumerate(pred_tensor):
                    if y > BUG_THRESHOLD:
                        #print("bug ",y, token_list[i])
                        bug_list.append(line_list[i])
            else:
                bug_list = []
            
            if len(bug_list):
                for i in bug_list:
                    predicted_results[fp].append(i)
            else:
                predicted_results[fp] = []
                
        # return the dictionary with file name as key and linelist as values 
        return dict(predicted_results)

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

    #####################################################
    #                                                   #
    #   1. Write your code below.                       #
    #   2. You may use the read_json_file() helper      #
    #      function to read a JSON file.                #
    #   3. Return a dict with the found bugs from here. #
    #                                                   #
    #####################################################
    #count = 0

    train = False
    max_len = 35
    if train:
        model.train_model(list_of_json_file_paths, token_embedding)
        return None
    else:
        predicted_results = defaultdict(list)
        frozen_model = model.load_model()
        frozen_model.eval()
        
        for fp in list_of_json_file_paths:
            #token_list, token_label, line_list,__,_ = find_bugs(fp, token_embedding)
            token_list, token_label, line_list,__,_  = get_token_from_AST.get_token(fp, False)
            bug_list = []
            fasttext_token = []

            if len(token_list):
                for line in token_list:
                    
                    if len(line) >= max_len:
                        line = line[0:max_len]
                        count_chop+=1
                    else:
                        while len(line) < max_len:
                          line.append("pad")                    

                    
                    linetoken = []
                    for token in line:
                        linetoken.append(token_embedding[token])
                    fasttext_token.append(torch.tensor(linetoken))

                padded = pad_sequence(fasttext_token, batch_first=True)
                #packed = pack_padded_sequence(padded,lengths=torch.tensor(35), batch_first=True, enforce_sorted=False)
                pred_y = frozen_model(padded)
                pred_tensor = torch.squeeze(pred_y,dim=1)

                tensor_bug_label = torch.tensor(token_label)
                
                for i, y in enumerate(pred_tensor):
                    if y > 0.70:
                        #print("bug ",y, token_list[i])
                        bug_list.append(line_list[i])
                    #else:
                        #print("no bug", y, tensor_bug_label[i], token_list[i])
            else:
                bug_list = []
            
            #count += len(bug_list)
        
            if len(bug_list):
                for i in bug_list:
                    predicted_results[fp].append(i)
            else:
                predicted_results[fp] = []
                
        #print("count : ",count)    
        return dict(predicted_results)

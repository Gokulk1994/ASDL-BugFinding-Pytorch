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
import model
from torch.nn.utils.rnn import pack_padded_sequence, pad_sequence

def read_json_file(json_file_path: str) -> List:
    """ Read a JSON file given path """
    try:
        obj_text = codecs.open(json_file_path, 'r',
                               encoding='utf-8').read()
        return json.loads(obj_text)
    except FileNotFoundError:
        print(
            "File {} not found. Please provide a correct file path Eg. ./results/hello.json".format(json_file_path))
        return []
    except Exception as e:
        print("invalid data file")
        # Most likely malformed JSON file
        return []

def all_if_as_bugs(json_file):

    data = read_json_file(json_file)

    if data == []:
        return []
    
    raw_code = data['raw_source_code']
    split_rawcode = raw_code.split("\n")
    ifcase_linenumber = []
    print(json_file)
    for i,line in enumerate(split_rawcode):
        if ('if (' in line) or ('if(' in line):
            ifcase_linenumber.append(i+1)
    return ifcase_linenumber


def evaluation(input_dir: str, out_file: str) -> None:
    if not input_dir and not out_file:
        write_json_file(data={}, file_path=out_file)
    try:
        list_of_json_file_paths: List = list(
            Path(input_dir).glob('**/*.json'))
        list_of_json_file_paths = [str(p) for p in list_of_json_file_paths]

        file_path_to_fast_text_embedding = os.path.join(
            input_dir, 'all_token_embedding.bin')

        if not os.path.exists(file_path_to_fast_text_embedding):
            print("Token embedding file is missing at {}".format(
                file_path_to_fast_text_embedding))
            return

        token_embedding = fasttext.load_model(
            path=file_path_to_fast_text_embedding)

        found_bugs: Dict[str, List[int]] = find_bugs_in_js_files(
            list_of_json_file_paths=list_of_json_file_paths, token_embedding=token_embedding)
        # Now write the found bugs to the JSON file

    except Exception as e:
        print(e)

    
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
    #count = 0
    predicted_results = defaultdict(list)
    frozen_model = model.load_model()
    frozen_model.eval()
    
    for fp in list_of_json_file_paths:
        token_list, token_label, line_list,__,_ = find_bugs(fp, token_embedding)
        bug_list = []
        fasttext_token = []

        if len(token_list):
            for line in token_list:
              linetoken = []
              for token in line:
                linetoken.append(token_embedding[token])
              fasttext_token.append(torch.tensor(linetoken))

            padded = pad_sequence(fasttext_token, batch_first=True)
            #packed = pack_padded_sequence(padded,lengths=torch.tensor(35), batch_first=True, enforce_sorted=False)
            pred_y = frozen_model(padded)
            pred_tensor = torch.squeeze(pred_y,dim=1)
            
            for i, y in enumerate(pred_tensor):
                if y > 0.65:
                    #print("bug ",y, token_list[i])
                    bug_list.append(line_list[i])
                #else:
                    #print("no bug", y, token_list[i])
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

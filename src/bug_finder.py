import get_token_from_AST
from typing import List, Dict
import argparse
from pathlib import Path

import json
import codecs

import sys
import os
import os.path
import fasttext
from collections import Counter

globaltype_count = Counter()
#"10055_7513_a_dynamicContent.json"

def write_json_file(data, file_path):
    try:
        #print("Writing JSON file "+file_path)
        json.dump(data, codecs.open(file_path, 'w', encoding='utf-8'),
                  separators=(',', ':'))
    except Exception as e:
        print(f"Could not write to {file_path} because {e}")


def find_bugs(file_path:str, token_embedding: fasttext.FastText):
    #print(file_path)
    token_list, token_label, line_list, type_list_pos,type_list_neg = get_token_from_AST.get_token(file_path)
    #print(len(line_list))
    """
    for i,token in enumerate(token_list):
        print(line_list[i])
        print(test_list[i])
        print(token)
        print(token_label[i])
        print("----------------------------")
    print("****************************************************************************")
    print("****************************************************************************")
    """

    return token_list, token_label, line_list, type_list_pos,type_list_neg

"""
def get_fasttext_embedding(token_list,token_embedding: fasttext.FastText):
    pass
    
def find_bugs_in_js_files(list_of_json_file_paths: List[str], token_embedding: fasttext.FastText) -> Dict[str, List[int]]:
    all_token_list  = []
    all_token_label = []
    all_line_list   = []
    globaltype_pos = Counter()
    globaltype_neg = Counter()
    filecount = 0
    
    for fp in list_of_json_file_paths:
        filecount += 1
        token_list, token_label, line_list,type_list_pos,type_list_neg = find_bugs(fp, token_embedding)
        all_token_list.append(token_list)
        all_token_label.append(token_label)
        all_line_list.append(line_list)

        for i in type_list_pos:
            globaltype_pos[i] += 1
        for j in type_list_neg:
            globaltype_neg[j] += 1

        if filecount == 500:
            print("500 files written")
            
            
            with open("token.txt", 'a', encoding="utf-8") as fp:
                for i in all_token_list:
                    fp.writelines("%s\n" % item  for item in i)                        
            with open("token_label.txt", 'a', encoding="utf-8") as fp:
                for i in all_token_label:
                    fp.writelines("%s\n" % item  for item in i)
            with open("line_list.txt", 'a', encoding="utf-8") as fp:
                for i in all_line_list:
                    fp.writelines("%s\n" % item  for item in i)
                    
            all_token_list  = []
            all_token_label = []
            all_line_list   = []
            filecount = 0

    write_json_file(globaltype_pos,"global_pos.json")
    write_json_file(globaltype_neg,"global_neg.json")
    return []
      
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


def run():
    input_dir = '../dataset/json_files/'
    output_dir = '.'
    out_file = os.path.join(output_dir, 'answer.json')
    evaluation(input_dir=input_dir,
               out_file=out_file)
    
if __name__ == '__main__':
    run()
"""

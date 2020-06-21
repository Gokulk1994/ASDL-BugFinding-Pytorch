"""
The evaluation script for asdl-bug-detection-project at Uni Stuttgart.

** As a participant, DO NOT modify this file. See run_bug_finding.py  **

Run this script as:
    python3 evaluation.py dataset_dir results_dir
        dataset_dir : The directory, that contains JSON files where bugs need to be found. It also contains the 
                      token embedding file called 'all_token_embedding.bin'
        results_dir : The directory, where a file called 'answer.json' will be written. This JSON file 
                      will contain the results of the bug finding. 
"""

from typing import List, Dict
import argparse
from pathlib import Path
import run_bug_finding
import json
import codecs

import sys
import os
import os.path
import fasttext


def write_json_file(data: Dict, file_path: str) -> None:
    try:
        # print("Writing JSON file "+file_path)
        json.dump(data, codecs.open(file_path, 'w', encoding='utf-8'),
                  separators=(',', ':'))
    except Exception as e:
        print(f"Could not write to {file_path} because {e}")


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

        found_bugs: Dict[str, List[int]] = run_bug_finding.find_bugs_in_js_files(
            list_of_json_file_paths=list_of_json_file_paths, token_embedding=token_embedding)
        # Now write the found bugs to the JSON file
        if found_bugs and isinstance(found_bugs, dict) and out_file and len(found_bugs) > 0:
            write_json_file(data=found_bugs, file_path=out_file)
    except Exception as e:
        print(e)


def run() -> None:
    if len(sys.argv) == 1:  # Use the default input and output directories if no arguments are provided
        return
    else:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
        out_file = os.path.join(output_dir, 'answer.json')
        evaluation(input_dir=input_dir,
                   out_file=out_file)


if __name__ == '__main__':
    run()

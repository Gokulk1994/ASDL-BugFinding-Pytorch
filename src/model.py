import torch  # -> version --> 1.5.0
import torch.nn as nn
import os
from bug_finder import find_bugs
import fasttext
from typing import List, Dict, Union, DefaultDict
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import numpy as np
import get_token_from_AST
from collections import Counter


import json
import codecs
from typing import List, Dict

def write_json_file(data, file_path):
    try:
        #print("Writing JSON file "+file_path)
        json.dump(data, codecs.open(file_path, 'w', encoding='utf-8'),
                  separators=(',', ':'))
    except Exception as e:
        print(f"Could not write to {file_path} because {e}")


class CreateDataSet(Dataset):
  def __init__(self, X, Y):
      self.X = X
      self.y = Y
      
  def __len__(self):
      return len(self.y)
  
  def __getitem__(self, idx):
      return torch.from_numpy(self.X[idx]),self.y[idx]

class BugFinderModel(nn.Module):
  def __init__(self, input_size, hidden_size, output_size,num_layers):
    super(BugFinderModel, self).__init__()

    self.lstm = nn.LSTM(input_size   = input_size, 
                          hidden_size= hidden_size,
                          num_layers = num_layers,
                          bias=False,
                          batch_first= True,
                        )
    self.dropout  = nn.Dropout(p=0.2)
    self.linear_1 = nn.Linear(hidden_size, 64,bias=False)
    self.tanh_1   = nn.Tanh()
    self.linear_2 = nn.Linear(64, output_size,bias=False)
    self.output   = nn.Sigmoid()

  def forward(self, input_feature):
    output_lstm, (hidden_op, cell_op) = self.lstm(input_feature)
    drop_out_layer = self.dropout(hidden_op[-1])

    linearop_1 = self.linear_1(drop_out_layer)
    lin_1_relu = self.tanh_1(linearop_1)
    
    linearop_2 = self.linear_2(lin_1_relu)
    prediction = self.output(linearop_2)

    return prediction
     
NUM_EPOCHS = 10
BATCH_SIZE = 32


def all_if_as_bugs(json_file):
    data = get_token_from_AST.read_json_file(json_file)
    if data != []:
      raw_code = data['raw_source_code']
      split_rawcode = raw_code.split("\n")
      ifcase_linenumber = []
      for i,line in enumerate(split_rawcode):
          if (('if (' in line) or ('if(' in line)) and '//' not in line and '/**' not in line and line[0] != '*' and '/*' not in line and '*' not in line:
              ifcase_linenumber.append(i+1)
      return len(ifcase_linenumber), ifcase_linenumber
    else:
      return -1, []

def load_model():
  cur_dir_path = os.path.dirname(os.path.realpath(__file__))
  saved_model_path = os.path.join(cur_dir_path, "trained_model.pt")
  loaded_model = torch.load(saved_model_path)

  return loaded_model

def save_token(list_of_json_file_paths, token_embedding):
  fasttext_token = []
  label_list = []
  line  = []

  all_token_list  = []
  all_token_label = []
  all_line_list   = []
  globaltype_pos = Counter()
  globaltype_neg = Counter()
  filecount = 0

  print("file count : ",len(list_of_json_file_paths))
  for fp in list_of_json_file_paths:
    filecount += 1
    token_list, token_label, line_list,type_list_pos,type_list_neg = get_token_from_AST.get_token(fp, True)
    #alllines, linenum = all_if_as_bugs(fp)
    if len(token_list):
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

    #for i,j in zip(token_list, token_label):
      #print(i,j)
    
    #if alllines > len(pos_list):  
    #print(fp, alllines,",",len(pos_list),",",len(neg_list))
    #print("------------------------------------------------")


    
    """
    if len(token_list):
      for lab in token_label:
        label_list.append(lab)
      
      for line in token_list:
        #print(line)
        linetoken = []
        for token in line:
          linetoken.append(token_embedding[token])
        
        if len(linetoken):
          fasttext_token.append(torch.tensor(linetoken))
        else:
          print("issue list : ", line)
  
    #print("---------------------------------------------------------")
    """
  """
  assert len(fasttext_token) == len(label_list)

  print(len(fasttext_token),len(label_list))
    
  #print("padding started")
  if len(fasttext_token):
    padded = pad_sequence(fasttext_token, batch_first=True)
    label  = torch.tensor(label_list)
  #print("padding ended")
  torch.save(padded, 'padded.pt')
  torch.save(label, 'label.pt')

  return padded, label
  """
  return [], []
def binary_accuracy(preds, y):
  rounded_preds = torch.round(preds)
  correct = (rounded_preds == y).float() 
  acc = correct.sum() / len(correct)
  return acc

def train(model, train_dl, optimizer, criterion):
  
  epoch_loss = 0
  epoch_acc = 0
  

  model.train()  
  print("Training started")
  Batch = 0
  for x, y in train_dl:

    Batch += 1

    optimizer.zero_grad()    
    
    predictions = model(x).squeeze()
    loss = criterion(predictions, y.float())        
    acc = binary_accuracy(predictions, y)   

    loss.backward()       
    optimizer.step()      
    
    epoch_loss += loss.item()  
    epoch_acc += acc.item()    
      
  return epoch_loss / len(train_dl), epoch_acc / len(train_dl)

def evaluate(model, valid_dl, criterion):

  epoch_loss = 0
  epoch_acc = 0


  model.eval()
  print("evaluation Started")
  Batch = 0

  with torch.no_grad():
    for x, y in valid_dl:
      Batch += 1
   
      predictions = model(x).squeeze()

      loss = criterion(predictions,y.float())
      acc = binary_accuracy(predictions, y)
      
      epoch_loss += loss.item()
      epoch_acc += acc.item()
    
  return epoch_loss / len(valid_dl), epoch_acc / len(valid_dl)


def train_model(list_of_json_file_paths: List[str], token_embedding: fasttext.FastText):
  
  if not os.path.exists('padded.pt'):
    input_feature, label = save_token(list_of_json_file_paths, token_embedding)
  else:
    input_feature = torch.load('padded.pt')
    label         = torch.load('label.pt')

  print("Padded size", input_feature.shape, label.shape, torch.sum(label))
  return 
  X_train, X_valid, y_train, y_valid = train_test_split(input_feature.numpy(), label.numpy(), test_size=0.2)
  train_ds = CreateDataSet(X_train, y_train)
  valid_ds = CreateDataSet(X_valid, y_valid)

  train_dl = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
  val_dl   = DataLoader(valid_ds, batch_size=BATCH_SIZE)

  new_model = BugFinderModel(input_size=100,hidden_size=100,output_size=1,num_layers=1)
  print(new_model)

  criterion = nn.BCELoss()
  optimizer = torch.optim.Adam(new_model.parameters(),lr = 0.001)

  for epoch in range(NUM_EPOCHS):

    print("Epoch : ",epoch)
    train_loss, train_acc = train(new_model, train_dl, optimizer, criterion)
  

    valid_loss, valid_acc = evaluate(new_model, val_dl, criterion)
    
    print(f'\tTrain Loss: {train_loss:.3f} | Train Acc: {train_acc*100:.2f}%')
    print(f'\t Val. Loss: {valid_loss:.3f} |  Val. Acc: {valid_acc*100:.2f}%')

  torch.save(new_model, 'trained_model.pt')
  torch.save(new_model.state_dict(), 'model_state.pt')


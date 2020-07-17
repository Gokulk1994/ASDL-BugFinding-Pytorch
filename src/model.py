import torch  # -> version --> 1.5.0
import torch.nn as nn
import os

import json
import codecs
import fasttext

from typing import List, Dict, Union, DefaultDict
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import numpy as np

import get_token_from_AST


NUM_EPOCHS       = 5   # Number of epochs
BATCH_SIZE       = 64   # batch size
TRAIN_TEST_SPLIT = 0.2  # split % of train data and test data
TRAIN_ALL        = True # Train with all input data. No splitting into validation data

def write_json_file(data, file_path):
    try:
        #print("Writing JSON file "+file_path)
        json.dump(data, codecs.open(file_path, 'w', encoding='utf-8'),
                  separators=(',', ':'))
    except Exception as e:
        print(f"Could not write to {file_path} because {e}")


"""
Class to create dataset as batches when using dataloader
"""
class CreateDataSet(Dataset):

  def __init__(self, X, Y):
    """
    Constructor : store the input feature and label
    """
    self.X = X
    self.y = Y

  def __len__(self):
    """
    returns the length of the samples
    """ 
    return len(self.y)
  

  def __getitem__(self, idx):
    """
    fetches the data samples from specific index
    """
    return torch.from_numpy(self.X[idx]),self.y[idx]


"""
Bug Finder model trained to predict the bugs in the model
"""
class BugFinderModel(nn.Module):

  def __init__(self, input_size, hidden_size, output_size,num_layers):
    """
    Define all layers and their parameters for this model
    """
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
    """
    Function will be called during forward pass of the model training
    provide input feature to the series of layer 
    """
    
    output_lstm, (hidden_op, cell_op) = self.lstm(input_feature)
    drop_out_layer = self.dropout(hidden_op[-1])

    linearop_1 = self.linear_1(drop_out_layer)
    lin_1_relu = self.tanh_1(linearop_1)
    
    linearop_2 = self.linear_2(lin_1_relu)
    prediction = self.output(linearop_2)

    return prediction
     


def load_model(model_name):
  """
  Load and return the provided model_name file
  """
  cur_dir_path = os.path.dirname(os.path.realpath(__file__))
  saved_model_path = os.path.join(cur_dir_path, model_name)
  loaded_model = torch.load(saved_model_path)

  return loaded_model

def save_token(list_of_json_file_paths, token_embedding, max_len):
  """
  Generate and save the token of each If condition from the given set of json_files
  """

  fasttext_token = []
  label_list = []
  line  = []

  print("file count : ",len(list_of_json_file_paths))
  
  for fp in list_of_json_file_paths:
    
    # get the token from AST tree
    token_list, token_label, _, __,___ = get_token_from_AST.get_token(fp, True)
    
    # add padding to token list when the length of token list is less than mas_len. If higher, then trim the token list
    if len(token_list):
      for lab in token_label:
        label_list.append(lab)
      
      for line in token_list:
        linetoken = []
        if len(line) >= max_len:
            line = line[0:max_len]
        else:
            while len(line) < max_len:
              line.append("_PAD")      

        for token in line:
          linetoken.append(token_embedding[token])
        
        if len(linetoken):
          fasttext_token.append(torch.tensor(linetoken))
        else:
          print("issue list : ", line)

  assert len(fasttext_token) == len(label_list)

  if len(fasttext_token):
    padded = pad_sequence(fasttext_token, batch_first=True)
    label  = torch.tensor(label_list)

  torch.save(padded, 'input_data.pt')
  torch.save(label, 'label.pt')

  return padded, label

def accuracy_estimation(prediction, actual):
  """
  Evaluate the accuracy of the model
  args : 
    prediction : predicted value from the model
    actual     : actual labels of the batch
  """
  correct = (torch.round(prediction) == actual).float() 
  accuracy = correct.sum() / len(correct)

  return accuracy

def train(model, train_dl, optimizer, criterion):
  """
  Forward pass of the model to train the network and learn the weights during backward pass using the optimizer
  args:
    model : generated binary classifier model
    train_dl : training data loaded using pytorch DataLoader
    optimizer : optimizer to be used during back propogation
    criterion : cost function to calculate loss value

  """

  total_loss = 0
  total_acc = 0
  
  # run model in training mode, so that some features like dropout will be enabled
  model.train()  

  print("Training in Progress....")


  for input_data, actual_label in train_dl:
    
    optimizer.zero_grad()    
    
    # predict values for input using forward pass
    predicted_label = model(input_data).squeeze()

    # Estimate Binary cross entropy loss
    loss = criterion(predicted_label, actual_label.float())        

    # find the accuracy of the model by comapring predicted and actual results
    accuracy = accuracy_estimation(predicted_label, actual_label)   

    # optimizing through back propogation
    loss.backward()       
    optimizer.step()      
    
    # accumulate the loss value to get average loss over all the epochs
    total_loss += loss.item()  
    total_acc  += accuracy.item()    
  
  print("Training completed")
      
  return total_loss / len(train_dl), total_acc / len(train_dl)

def evaluate(model, valid_dl, criterion):
  """
  Evaluate the performance of the model with test data samples
  args:
    model : generated binary classifier model
    train_dl : training data loaded using pytorch DataLoader
    optimizer : optimizer to be used during back propogation
    criterion : cost function to calculate loss value

  """
  total_loss = 0
  total_acc = 0

  # run model in evaluate mode, so that some features like dropout will be disabled
  model.eval()

  print("Evaluation in progress")

  # stop optimization of network
  with torch.no_grad():
    for input_data, actual_label in valid_dl:
      
      # predict values for test data using forward pass
      predicted_label = model(input_data).squeeze()

      # Estimate Binary cross entropy loss
      loss = criterion(predicted_label,actual_label.float())

      # find the accuracy of the model by comparing predicted and actual results
      accuracy = accuracy_estimation(predicted_label, actual_label)
      
      # accumulate the loss value to get average loss over all the epochs
      total_loss += loss.item()
      total_acc += accuracy.item()
  print("Evaluation completed")
  return total_loss / len(valid_dl), total_acc / len(valid_dl)


def train_model(list_of_json_file_paths: List[str], token_embedding: fasttext.FastText, max_len = 35):

  """
  Generate token, split train and test set, train and validate the model
  args:
    list_of_json_file_paths : list of json file path
    token_embedding : fasttext token embedding to convert text to tokens
    max_len : allowed maximum length of tokens for a condition

  """

  # if data is not available, geenrate tokens from json_file, else use the available data
  if not os.path.exists('input_data.pt'):
    input_feature, label = save_token(list_of_json_file_paths, token_embedding, max_len)
  else:
    input_feature = torch.load('input_data.pt')
    label         = torch.load('label.pt')

  print("Input data size", input_feature.shape, label.shape, torch.sum(label))

  # split the data into train and test based on TRAIN_TEST_SPLIT ratio
  X_train, X_valid, y_train, y_valid = train_test_split(input_feature.numpy(), label.numpy(), test_size=TRAIN_TEST_SPLIT)
  
  if not TRAIN_ALL:
    # create the dataset class for the input feature
    train_ds = CreateDataSet(X_train, y_train)
    valid_ds = CreateDataSet(X_valid, y_valid)

    # Split the data into batches and shuffle 
    train_dl = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_dl   = DataLoader(valid_ds, batch_size=BATCH_SIZE)
  else:
    all_data_ds = CreateDataSet(input_feature.numpy(), label)
    all_data_dl = DataLoader(all_data_ds, batch_size=BATCH_SIZE)

  # bug finder model
  bug_finder = BugFinderModel(input_size=100,hidden_size=100,output_size=1,num_layers=1)
  print(bug_finder)

  # binary cross entropy loss 
  criterion = nn.BCELoss()
  optimizer = torch.optim.Adam(bug_finder.parameters(),lr = 0.001)

  for epoch in range(NUM_EPOCHS):

    print("Current Epoch : ",epoch)

    if not TRAIN_ALL:
      # Training the model using train data
      train_loss, train_acc = train(bug_finder, train_dl, optimizer, criterion)
      
      # evaluating using validation data
      valid_loss, valid_acc = evaluate(bug_finder, val_dl, criterion)
  
      print(f'\tTrain  Loss: {train_loss:.3f} | Train Acc : {train_acc*100:.2f}%')
      print(f'\tValid. Loss: {valid_loss:.3f} | Valid. Acc: {valid_acc*100:.2f}%')
    else:
      # Training the model using all the input data
      all_train_loss, all_train_acc = train(bug_finder, all_data_dl, optimizer, criterion)
      
      print(f'\tTrain  Loss: {all_train_loss:.3f} | Train Acc : {all_train_acc*100:.2f}%')
      

  # save the trained model
  torch.save(bug_finder, 'trained_model.pt')
  torch.save(bug_finder.state_dict(), 'model_state.pt')


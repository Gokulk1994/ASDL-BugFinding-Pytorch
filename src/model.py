import torch  # -> version --> 1.5.0
import torch.nn as nn
import os



class BugFinderModel(nn.Module):
  def __init__(self, input_size, hidden_size, output_size,num_layers):
    super(BugFinderModel, self).__init__()

    self.lstm = nn.LSTM(input_size   = input_size, 
                          hidden_size= hidden_size,
                          num_layers = num_layers,
                          bias=True,
                          batch_first= True,
                          dropout = 0.2
                        )
    self.linear_1 = nn.Linear(hidden_size, 128,bias=True)
    self.linear_2 = nn.Linear(128, 64,bias=True)
    self.linear_3 = nn.Linear(64, 32,bias=True)
    self.linear_4 = nn.Linear(32, output_size,bias=True)
    self.Relu_1   = nn.Tanh()
    self.Relu_2   = nn.Tanh()
    self.Relu_3   = nn.Tanh()
    self.output = nn.Sigmoid()

  def forward(self, input_feature):
    output_lstm, (hidden_op, cell_op) = self.lstm(input_feature)
    
    linearop_1 = self.linear_1(hidden_op[-1])
    lin_1_relu = self.Relu_1(linearop_1)

    linearop_2 = self.linear_2(lin_1_relu)
    lin_2_relu = self.Relu_2(linearop_2)

    linearop_3 = self.linear_3(lin_2_relu)
    lin_3_relu = self.Relu_3(linearop_3)

    linearop_4 = self.linear_4(lin_3_relu)
    prediction = self.output(linearop_4)

    return prediction
     
     


def load_model():
    cur_dir_path = os.path.dirname(os.path.realpath(__file__))
    saved_model_path = os.path.join(cur_dir_path, "trained_model.pt")
    loaded_model = torch.load(saved_model_path)

    return loaded_model

    

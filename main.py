import os
import numpy as np
import pandas as pd
import email
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
import keras_metrics

tokenizer = Tokenizer()

# load json and create model
json_file = open('model/lstm_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights('model/lstm_model.h5')
print('Loaded model from disk')

def get_predictions(text):
  sequence = tokenizer.texts_to_sequences([text])
  # pad the sequence
  sequence = pad_sequences(sequence, maxlen=100)
  # get the prediction
  prediction = loaded_model.predict(sequence)[0]
  # one-hot encoded vector, revert using np.argmax
  if np.argmax(prediction) == 0:
    print('The email has not been flagged as SPAM.')
  else:
    print('The email has been flagged as SPAM.')

text = "This is just to let you all know we have scheduled a meet"
get_predictions(text)

text = "Congratulations! You've won a $1,000 Walmart gift card. Go to http://www.walmart.xyz/claim-reward-1000-dollars to claim now!"
get_predictions(text)
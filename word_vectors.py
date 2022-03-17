import numpy as np

# Download pretrained word vectors
# https://nlp.stanford.edu/data/glove.6B.zip

# follow instructions here:
# https://medium.com/analytics-vidhya/basics-of-using-pre-trained-glove-vectors-in-python-d38905f356db
embeddings_dict = {}

# TODO
# * download and unzip glove vectors
# * make embeddings dict so that the keys are the words
#   and the values are the word vectors
# * get average sentence vectors for each sentence in the corpus
with open("glove.6B.50d.txt", 'r', encoding="utf-8") as f:
  for line in f:
    word, vector = line.split(" ", 1)
    vector = np.fromstring(vector, dtype = float, sep = " ")
    break

corpus = [
  "hello",
  "goodbye",
  "my name"
]
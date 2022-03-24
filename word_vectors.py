import numpy as np


# Download pretrained word vectors
# https://nlp.stanford.edu/data/glove.6B.zip

# follow instructions here:
# https://medium.com/analytics-vidhya/basics-of-using-pre-trained-glove-vectors-in-python-d38905f356db

# TODO
# * download and unzip glove vectors
# * make embeddings dict so that the keys are the words
#   and the values are the word vectors
embeddings_dict = {}
# * get average sentence vectors for each sentence in the corpus
with open("glove.6B/glove.6B.50d.txt", 'r', encoding="utf-8") as f:
  for line in f:
    word, vector = line.split(" ", 1)
    vector = np.fromstring(vector, dtype = float, sep = " ")
    embeddings_dict.update({word: vector})

corpus = [
  "hello",
  "goodbye",
  "my name is xyz123asdflk"
]

sentence_vectors = []
for sentence in corpus:
  print(sentence)
  word_vectors = []
  for word in sentence.split():
    # print(word)
    if word in embeddings_dict:
      vector = embeddings_dict[word]
      # print(vector)
      word_vectors.append(vector)
  sentence_matrix = np.stack(word_vectors)
  sentence_vector = sentence_matrix.mean(axis = 0)
  sentence_vectors.append(sentence_vector)
  # print(sentence_matrix)
  # print(sentence_vectors)
corpus_matrix = np.stack(sentence_vectors)
print(corpus_matrix)


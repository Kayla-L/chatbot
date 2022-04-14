import pandas as pd
import re
import word_vectors
from scipy.spatial.distance import cosine
import numpy as np

# For ever word that ever appears in the stories we entered,
# this will count how many times each word appears in
# each sentence. The rows are sentences, and the columns are
# words.
from sklearn.feature_extraction.text import CountVectorizer
# Starts with the count vectorizer and THEN rescales so that
# seeing boring words like "the" doesn't make a difference
# but seeing unique words like "unicorn" would make a
# difference
"""
"tf-idf" means "term frequency inverse document frequency"
numerator: number of times the word shows up in the sentence
denominator: number of sentences that word appear in
"""
from sklearn.feature_extraction.text import TfidfVectorizer

# given two sentence represented as vectors, how similar
# are they
from sklearn.metrics.pairwise import cosine_similarity

# import texthero as hero
# from texthero import preprocessing

# import sqlite3
# [x] get a corpus of example conversation

import spacy

# TODO: define function get_clean_sentence
# clean_sentence = get_clean_sentence(sentence)
def get_clean_sentence(sentence):
  # lower case everything 
  new_sentence = sentence.lower()
  # turn new lines into spaces
  new_sentence = re.sub("\\n", " ", new_sentence)
    # get rid of anything that's not a number, letter or space
  new_sentence = re.sub("[^a-z0-9 ]", "", new_sentence)
  # remove whitespace at the beginning and end of the sentence
  new_sentence = new_sentence.strip()
  # if there's more than one space in a row, 
  new_sentence = re.sub("\\s+", " ", new_sentence)
  return new_sentence

# poe_corpus is a pandas dataframe
poe_corpus = pd.read_csv("poe_stories.csv")
# poe_stories is a pandas series
poe_stories = poe_corpus["text"]

sentences = []
# we separate each chapter into sentences and make a
# list of sentences
for chapter in poe_stories:
  sentences += re.split("[.?!]", chapter)
clean_sentences = []
# we clean up each sentence to be easier to deal with
for sentence in sentences:

  clean_sentence = get_clean_sentence(sentence)

  if re.search("(said|replied|answered|declared)", clean_sentence):
    pass
  else:
    clean_sentences.append(clean_sentence)

# # create the transform
# vectorizer = TfidfVectorizer()
# # tokenize and build vocab
# # This is where it learns all the unique words that ever show
# # up in the corpus.
# vectorizer.fit(clean_sentences)
# # encode document
# vectors = vectorizer.transform(clean_sentences)
# # # summarize encoded vector
# # print(vectors.shape)
# # print(type(vectors))
# # print(vectors.toarray())

# Load the spacy model that you have installed
nlp = spacy.load('en_core_web_sm')
# process a sentence using the model

def get_vector(sentence):
  doc = nlp(sentence)
  # It's that simple - all of the vectors and words are assigned after this point
  # Get the mean vector for the entire sentence (useful for sentence classification etc.)
  return doc.vector

# vectors = []
# for sentence in clean_sentences[:100]:
#   vector = get_vector(sentence)
#   vectors.append(vector)

corpus_embeddings = word_vectors.get_sentence_vectors(clean_sentences)
input_sentence_to_chatbot = "it is a beautiful day today"
print(input_sentence_to_chatbot)
input_sentence_vector = word_vectors.get_sentence_vectors([input_sentence_to_chatbot])[0]


# input_sentence_vector = vectorizer.transform(
  # input_sentence_to_chatbot)
# input_sentence_vector = [get_vector(input_sentence_to_chatbot[0])]
# print(input_sentence_vector)
# print(vectorizer.vocabulary_["good"])
# print(vectorizer.vocabulary_["night"])

# Finding the best matching sentence to the input
# cosine_similarities = cosine_similarity(vectors, input_sentence_vector).flatten()
# best_match_index = cosine_similarities.argmax()

def cosine_distances(embedding_matrix, extracted_embedding):
  return cosine(embedding_matrix, extracted_embedding)
cosine_distances = np.vectorize(cosine_distances, signature='(m),(d)->()')

cosine_similarities = 1-cosine_distances(corpus_embeddings, input_sentence_vector)
# print(cosine_similarities)
best_match_index = cosine_similarities.argmax()
# print(best_match_index)

print("best match in corpus:", [clean_sentences[best_match_index]])
print("chatbot response:", clean_sentences[best_match_index + 1])

# print(corpus_embeddings[500])
# print(input_sentence_vector)
# print(len(clean_sentences))
# print(corpus_embeddings.shape)
# print(corpus_embeddings[best_match_index])
# print(word_vectors.embeddings_dict["nitre"])

# conn = sqlite3.connect("classical_literature.db")
# classical_corpus = pd.read_sql("select * from text_files", conn)
# #classical_corpus_html = classical_corpus.loc[classical_corpus.fmt == "html"]
# classical_corpus_txt = classical_corpus.loc[classical_corpus.fmt == "txt"]
# classical_chapters = classical_corpus_txt["text"]
# sentences = []
# for chapter in classical_chapters:
#   sentences += chapter.split("[.?!]")

# print(sentences[:10])

# bible_corpus = pd.read_csv("bible/t_wbt.csv")
# bible_sentences = bible_corpus["t"]

# custom_pipeline = [preprocessing.fillna,
#                    #preprocessing.lowercase,
#                    preprocessing.remove_whitespace,
#                    preprocessing.remove_diacritics
#                    #preprocessing.remove_brackets
#                   ]
# bible_corpus['clean_text'] = hero.clean(bible_corpus['t'], custom_pipeline)
# print(bible_corpus)
# print(bible_sentences[0])
# # bible_corpus['clean_text'] = [n.replace('{','') for n in df['clean_text']]
# # bible_corpus['clean_text'] = [n.replace('}','') for n in df['clean_text']]
# # bible_corpus['clean_text'] = [n.replace('(','') for n in df['clean_text']]
# # bible_corpus['clean_text'] = [n.replace(')','') for n in df['clean_text']]

# find the closest match in the corpus given the utterance

#  bag of words similarity model (order of words in sentence doesn't matter)
#  each word is a bunch of numbers (a vector)
#  the whole sentence is going to be the average of those numbers

# return the response to the closest match




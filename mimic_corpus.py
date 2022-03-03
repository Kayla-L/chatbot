import pandas as pd
import re

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

  # # TODO: define function get_clean_sentence
  # clean_sentence = get_clean_sentence(sentence)

  # lower case everything
  clean_sentence = sentence.lower()
  # turn new lines into spaces
  clean_sentence = re.sub("\\n", " ", clean_sentence)
  # get rid of anything that's not a number, letter or space
  clean_sentence = re.sub("[^a-z0-9 ]", "", clean_sentence)
  # remove whitespace at the beginning and end of the sentence
  clean_sentence = clean_sentence.strip()
  # if there's more than one space in a row, 
  clean_sentence = re.sub("\\s+", " ", clean_sentence)



  if re.search("(said|replied|answered|declared)", clean_sentence):
    pass
  else:
    clean_sentences.append(clean_sentence)

# create the transform
vectorizer = TfidfVectorizer()
# tokenize and build vocab
# This is where it learns all the unique words that ever show
# up in the corpus.
vectorizer.fit(clean_sentences)
# encode document
vectors = vectorizer.transform(clean_sentences)
# # summarize encoded vector
# print(vectors.shape)
# print(type(vectors))
# print(vectors.toarray())

input_sentence_to_chatbot = ["it is a beautiful day today"]
input_sentence_vector = vectorizer.transform(
  input_sentence_to_chatbot)
# print(input_sentence_vector)
# print(vectorizer.vocabulary_["good"])
# print(vectorizer.vocabulary_["night"])

# Finding the best matching sentence to the input
cosine_similarities = cosine_similarity(vectors, input_sentence_vector).flatten()
best_match_index = cosine_similarities.argmax()

print(clean_sentences[best_match_index])
print(clean_sentences[best_match_index + 1])

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


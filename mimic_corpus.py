import pandas as pd
# [x] get a corpus of example conversation

# poe_corpus is a pandas dataframe
poe_corpus = pd.read_csv("preprocessed_data.csv")
# poe_stories is a pandas series
poe_stories = poe_corpus["text"]
print(poe_stories)
# find the closest match in the corpus given the utterance

#  bag of words similarity model (order of words in sentence doesn't matter)
#  each word is a bunch of numbers (a vector)
#  the whole sentence is going to be the average of those numbers

# return the response to the closest match
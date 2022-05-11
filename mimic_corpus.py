import pandas as pd
import re
import word_vectors
from scipy.spatial.distance import cosine
import numpy as np

# clean_sentence = get_clean_sentence(sentence)
def get_clean_sentence(sentence):
  # lower case everything 
  new_sentence = sentence.lower()
  # turn new lines into spaces
  new_sentence = re.sub("\\n", " ", new_sentence)
    # get rid of anything that's not a number, letter or space
  new_sentence = re.sub("[^a-z0-9 ]", " ", new_sentence)
  # remove whitespace at the beginning and end of the sentence
  new_sentence = new_sentence.strip()
  # if there's more than one space in a row, 
  new_sentence = re.sub("\\s+", " ", new_sentence)
  return new_sentence



# conn = sqlite3.connect("classical_literature.db")
# classical_corpus = pd.read_sql("select * from text_files", conn)
# #classical_corpus_html = classical_corpus.loc[classical_corpus.fmt == "html"]
# classical_corpus_txt = classical_corpus.loc[classical_corpus.fmt == "txt"]
# classical_chapters = classical_corpus_txt["text"]
# sentences = []
# for chapter in classical_chapters:
#   sentences += chapter.split("[.?!]")




class MimicCorpus():
  def __init__(self, source_text):
    if source_text == "poe":
      self.clean_sentences = self.setup_poe_corpus()
    elif source_text == "bible":
      self.clean_sentences = self.setup_bible_corpus()
    elif source_text == "both":
      poe_sentences = self.setup_poe_corpus()
      bible_sentences = self.setup_bible_corpus()
      self.clean_sentences = poe_sentences + bible_sentences
    else:
      print("What source should I use for the mimic corpus????")
    self.corpus_embeddings = word_vectors.get_sentence_vectors(
      self.clean_sentences
    )
  def get_chatbot_response(self, input_sentence_to_chatbot):
    input_sentence_vector = word_vectors.get_sentence_vectors(
      [input_sentence_to_chatbot]
    )[0]

    # Finding the best matching sentence to the input

    def cosine_distances(embedding_matrix, extracted_embedding):
      return cosine(embedding_matrix, extracted_embedding)

    cosine_distances = np.vectorize(cosine_distances, signature='(m),(d)->()')

    cosine_similarities = 1-cosine_distances(
      self.corpus_embeddings,
      input_sentence_vector
    )
    best_match_index = cosine_similarities.argmax()

    best_match_in_corpus = self.clean_sentences[best_match_index]
    chatbot_response = self.clean_sentences[best_match_index + 1]

    return chatbot_response

  """
  This function reads the Poe Corpus and cleans up all the sentences.
  Later on, those sentences can be used in other functions inside of this
  class.
  """
  def setup_poe_corpus(self):
    # poe_corpus is a pandas dataframe
    poe_corpus = pd.read_csv("poe_stories.csv")
    # poe_stories is a pandas series
    poe_stories = poe_corpus["text"]

    sentences = []
    # we separate each chapter into sentences and make a
    # list of sentences
    for chapter in poe_stories:
      sentences += re.split("[.?!]", chapter)

    clean_sentences = self.clean_all_sentences(sentences)

    return clean_sentences
  """
  Given a list of sentences pulled from whatever text, this function
  will reduce the sentences to all lowercase and no punctuation
  """
  def clean_all_sentences(self, raw_sentences):

    clean_sentences = []
    # we clean up each sentence to be easier to deal with
    for sentence in raw_sentences:

      clean_sentence = get_clean_sentence(sentence)

      if re.search("(said|replied|answered|declared|remarked|exclaimed)", clean_sentence):
        pass
      else:
        clean_sentences.append(clean_sentence)
    return clean_sentences

  def setup_bible_corpus(self):
    bible_corpus = pd.read_csv("bible/t_wbt.csv")
    bible_sentences = bible_corpus["t"]
    clean_sentences = self.clean_all_sentences(bible_sentences)
    return clean_sentences

# chatbot

## Mimic corpus

Let the chatbot respond to *anything* with the "most appropriate" response from a given corpus.

Classical corpora:

- https://www.kaggle.com/leangab/poe-short-stories-corpuscsv
- https://www.kaggle.com/nltkdata/shakespeare
- https://www.kaggle.com/charlesaverill/gothic-literature
- https://www.kaggle.com/raynardj/classic-english-literature-corpus?select=books.db
- https://www.kaggle.com/oswinrh/bible 

TODO:

1. [x] find corpora
2. [ ] preprocess corpora into vector (i.e. a bunch of numbers)
    a. [ ] break the corpus up into sentences
    b. [ ] for each sentence:
        - [ ] break the sentence up into words
        - [ ] for each word, convert the word to a vector (i.e. a bunch of numbers)
        - [ ] average together all the word vectors
3. [ ] when we get the user utterance, change that to numbers
4. [ ] find the closest set of numbers in the corpus to the user utterance

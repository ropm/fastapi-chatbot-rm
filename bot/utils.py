import nltk
import numpy
from nltk.stem.porter import PorterStemmer


class NaturalLangProcessor:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def tokenize(self, sentence):
        '''
        Tokenizes a sentence, creates a list of all the words.
        If this doesnt work the first  time, ntlk needs punkt data (see train.py)
        '''
        return nltk.word_tokenize(sentence)

    def stem(self, word):
        return self.stemmer.stem(word.lower())

    def bag_of_words(self, tokenized_sentence, all_words):
        tokenized_sentence = [self.stem(w) for w in tokenized_sentence]
        # have only zeroes in bag at first
        bag = numpy.zeros(len(all_words), dtype=numpy.float32)
        for idx, w in enumerate(all_words):
            # if word found in sentence, tag it as 1
            if w in tokenized_sentence:
                bag[idx] = 1.0
        return bag

    def dl_punkt(self):
        nltk.download('punkt')

import nltk
from nltk.stem.porter import PorterStemmer
# nltk.download('punkt')


class NaturalLangProcessor:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def tokenize(self, sentence):
        '''
        Tokenizes a sentence, creates a list of all the words.
        If this doesnt work the first  time, uncomment the download above
        '''
        return nltk.word_tokenize(sentence)

    def stem(self, word):
        return self.stemmer.stem(word.lower())

    def bag_of_words(self, tokenized_sentence, all_words):
        pass
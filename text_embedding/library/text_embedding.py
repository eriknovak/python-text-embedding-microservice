###########################################################
# Text Embedding Model
# The model creates text embedding in two ways:
# 1. Averaging the word embeddings in the text
# 2. First do the (1) approach and then remove the most
#    common information with the calculated projection
#    matrix (link: https://openreview.net/pdf?id=SyK00v5xx)

# for directory creation
import os

# for model loading
import pickle

# used for model loading and processing text
from gensim.models import KeyedVectors, FastText
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation
from langdetect import detect

# used for calculating the projection matrix
from sklearn.decomposition import PCA

# utility libraries
import numpy as np
import operator

class TextEmbedding:

    def __init__(self, language, model_path, model_format='word2vec'):
        """Initializes the text embedding module

        Args:
            language (str): The language of the embedding model.
                It must be in the ISO 693-1 code format.
            model_path (str): The path to the embedding model file.
            model_format (str): The format in which the model file is stored.
                Possible options are 'word2vec' and 'fasttext'. (Default = 'word2vec')

        """
        self.__language = language
        self.__embedding = None
        self.__model = None
        # projection matrix used for
        self.__projection_matrix = None

        if not model_path == None:
            if os.path.isfile(model_path):
                self.__load_model(model_path, model_format)
        else:
            raise Exception("TextEmbedding.__init__: model_path does not exist {}".format(model_path))


    def __load_model(self, model_path, model_format):
        """Loads the word embedding model

        Args:
            model_path (str): The word embedding model path.
            model_format (str): The word embedding model format.

        """

        if model_format == 'word2vec':
            # load the model with the word2vec format
            self.__model = KeyedVectors
            self.__embedding = self.__model.load_word2vec_format(model_path)
            self.__stopwords = self.stopwords()
        elif model_format == 'fasttext':
            # load the model with the fasttext format
            self.__model = FastText
            self.__embedding = self.__model.load(model_path)
            self.__stopwords = self.stopwords()
        else:
            raise Exception("TextEmbedding.__load_model: Model '{}' not supported (must be 'word2vec' or 'fastfext').".format(model_format) +
                            " Cannot load word embedding model.")

        # calculate the default projection matrix
        v = np.zeros(self.__embedding.vector_size, dtype=np.float32)
        self.__projection_matrix = np.outer(v, v)


    def get_language(self):
        """Returns the language of the text embedding model

        Returns:
            str: The ISO 693-1 code of the language.

        """

        return self.__language


    def stopwords(self):
        """Retrieve the stopwords corresponding to the model language

        Returns:
            list(str): A list of stopwords.

        """

        # create stopword file path
        fname = "./data/stopwords/{}.stopwords.txt".format(self.__language)

        # check if the file exists
        if not os.path.isfile(fname):
            print("No stopword list for language {}".format(self.__language))
            return []

        # retrieve stopwords based on the language
        with open(fname, 'r', encoding='utf-8') as f:
            stopwords = f.readlines()

        # strip the stopwords of any access whitespaces
        stopwords = [x.strip() for x in stopwords]

        # return the stopwords for the corresponding language
        return stopwords


    def tokenize(self, text):
        """Tokenizes the provided text

        Args:
            text (str): The text to be tokenized

        Returns:
            list(tuple(str, int)): A list of (token, count) pairs from the text without the stopwords.

        """

        # make everything lowercase and strip punctuation
        CUSTOM_FILTERS = [lambda x: x.lower(), strip_punctuation]
        tokens = preprocess_string(text, CUSTOM_FILTERS)

        # filter out all stopwords
        filtered_tokens = [w for w in tokens if not w in self.__stopwords]

        # count the term frequency in the text
        count = { }
        for word in filtered_tokens:
            if word not in count:
                count[word] = 0
            count[word] += 1

        # sort the terms in descending order
        terms_sorted = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
        return terms_sorted


    def text_embedding(self, text, language=None):
        """Create the text embedding

        Args:
            text (str): The text to be embedded

        Returns:
            list(float): The array of values representing the text embedding

        """

        # check if the provided text is the one the embedding can perform
        text_language = language if language != None else detect(text)
        if not text_language == self.__language:
            # raise an exeption of not matching languages
            raise Exception("The provided text is not valid. Text language ({}) != {}".format(text_language, self.__language))

        # prepare the embedding placeholder
        embedding = np.zeros(self.__embedding.vector_size, dtype=np.float32)

        if text is None:
            # return the default embedding in a vanilla python object
            return embedding.tolist()

        # get the text terms with frequencies
        term_sorted = self.tokenize(text)
        # iterate through the terms and count the number of terms
        count = 0
        for token, number_of_appearances in term_sorted:
            # sum all token embeddings of the vector
            if token in self.__embedding.vocab.keys():
                embedding += self.__embedding[token] * number_of_appearances
                count += number_of_appearances

        if count == 0:
            # return the empty embedding list
            return embedding.tolist()

        # average the embedding
        __text_embedding = embedding / count

        # (2) remove the projection on the first singular vector
        __text_embedding = __text_embedding - self.__projection_matrix.dot(__text_embedding)

        # return the embedding in vanilla python object
        return __text_embedding.tolist()


    def __train_projection_matrix(self, matrix):
        """Trains the PCA for retrieving the first singular vector and
        generating the projection matrix.

        Args:
            matrix (list(list(float))): The matrix of text embeddings.

        """

        # set the PCA parameters and fit the model
        pca = PCA(n_components=1)
        pca.fit(matrix)
        # get the first singular vector and get the projection matrix
        sv = pca.components_[0]
        self.__projection_matrix = np.outer(sv, sv)


    def save_projection_matrix(self, path):
        """Saves the projection matrix

        Args:
            path (str): The path where the matrix will be stored.

        """

        with open(path, 'wb') as output:
            pickle.dump(self.__projection_matrix, output, pickle.HIGHEST_PROTOCOL)




    def load_projection_matrix(self, path):
        """Loads the projection matrix

        Args:
            path (str): The path where the matrix is located.

        """

        if not path == None:
            if os.path.isfile(path):
                with open(path, 'rb') as input:
                    self.__projection_matrix = pickle.load(input)
        else:
            raise Exception("TextEmbedding.load_projection_matrix: path does not exist {}".format(path))


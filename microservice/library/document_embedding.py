# TODO import correct module for word embeddings

class TextEmbedding:

    def __init__(self, language, model_path):
        self.language = language
        self.model = self.load_model(model_path)


    def load_model(self, model_path):
        """Loads the word embedding model

        Args:
            model_path (str): The word embedding model path.

        Returns:
            obj: The word embedding model

        """
        # TODO write the body of the function
        return None


    def stopwords(self, language):
        # TODO write the body of the function
        return None


    def tokenize(self, keywords):
        # TODO write the body of the function
        return None


    def document_embedding(self, text):
        # TODO write the body of the function
        return None
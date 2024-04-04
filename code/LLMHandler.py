import abc
class LLMHandler(abc.ABC):
    @abc.abstractmethod
    def generate_embeddings(self, data):
        pass
    @abc.abstractmethod
    def get_response_from_model(self, data):
        pass

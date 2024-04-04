import abc

class VectorDBHandler(abc.ABC):
    @abc.abstractmethod
    def store_vector_data(self, data, settings):
        pass
    @abc.abstractmethod
    def do_vector_search(self, input_vector, settings):
        pass
    @abc.abstractmethod
    def init_vector_storage(self,config_data):
        pass
    @abc.abstractmethod
    def connect_to_vector_store(self, config_data):
        pass
    @abc.abstractmethod
    def reset_db(self, config_data):
        pass
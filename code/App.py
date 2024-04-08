from CosmosDBPyMongoVectorHandler import CosmosDBPyMongoVectorHandler
from LLMHandler import LLMHandler
from AOAIHandler import AOAIHandler
from VectorDBHandler import VectorDBHandler
from Config import Config
class App:
    def __init__(self,app_config_path):
        self.app_config = Config(app_config_path)
        (self.vector_db_handler,self.vector_db_config) = self.init_vector_db(self.app_config)
        (self.llm_handler,self.llm_config) = self.init_LLM(self.app_config)   

    def insert_data(self, data):
        self.vector_db_handler.store_vector_data(data)
    def do_init(self):
        self.vector_db_handler.reset_db(self.vector_db_config.config_data)
        self.vector_db_handler.init_vector_storage(self.vector_db_config.config_data)
        return True
    def run_test(self):
        test_query = "What is a test?"
        test_vector = self.llm_handler.generate_embeddings(test_query)
        results = self.vector_db_handler.do_vector_search(test_vector,self.app_config.config_data)
        for result in results:
            current_result_content = result["content"]
            print("Result: "+current_result_content)
    def init_vector_db(self,app_config): 
        vector_db_handler = None
        vector_db_config = None
        if (app_config.config_data["vector_storage_mode"] == "ALL"):
            cosmos_db_config_path = app_config.config_data["cosmos_db_config_path"]
            vector_db_config = Config(cosmos_db_config_path)
            vector_db_handler =  self.init_cosmos_db(vector_db_config)
        return (vector_db_handler, vector_db_config)

    def init_LLM(self,app_config)->LLMHandler:
        llm_handler = None
        llm_config = None
        if (app_config.config_data["LLM"] == "AOAI"):
            aoai_config_path = app_config.config_data["aoai_config_path"]
            llm_config = Config(aoai_config_path)
            llm_handler = self.init_AOAI(llm_config)
        return (llm_handler, llm_config)

    def init_AOAI(self,config):
        aoai_endpoint = config.config_data["aoai_endpoint"]
        aoai_key = config.config_data["aoai_key"]
        aoai_api_version = config.config_data["aoai_api_version"]
        aoai_temperature = config.config_data["aoai_temperature"]
        aoai_model = config.config_data["aoai_deployment_name"]
        aoai_handler = AOAIHandler(aoai_endpoint, aoai_key, aoai_api_version, aoai_temperature, aoai_model)
        return aoai_handler
    def init_cosmos_db(self,config):
        cosmos_username = config.config_data["cosmos_username"]
        cosmos_password = config.config_data["cosmos_password"]
        cosmos_server = config.config_data["cosmos_server"]
        cosmos_vector_handler = CosmosDBPyMongoVectorHandler(cosmos_username, cosmos_password, cosmos_server)
        return cosmos_vector_handler
    
from VectorDBHandler import VectorDBHandler
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from Config import Config
from Utilities import Utils
from azure.search.documents.indexes.models import (
        SearchIndex,
        SearchField,
        SearchFieldDataType,
        SimpleField,
        SearchableField,
        VectorSearch,
        VectorSearchProfile,
        HnswAlgorithmConfiguration,
    )

class AzureSearchVectorHandler(VectorDBHandler):
    def __init__(self, config_data):
        self.search_service_endpoint = config_data["search_service_endpoint"]
        self.search_service_key = config_data["search_service_key"]
        self.search_index_name = config_data["search_index_name"]
        self.data_schema = Config(config_data["data_schema_path"]).config_data
        self.credentials = AzureKeyCredential(self.search_service_key)
        connection_result = self.connect_to_vector_store()
        if connection_result:
            print("Connected to Azure Search Index successfully")
        else:
            exception_message = "Failed to connect to Azure Search Index"
            raise Exception(exception_message)
    def connect_to_vector_store(self):
        self.search_index_client = SearchIndexClient(endpoint=self.search_service_endpoint, 
                                        index_name=self.search_index_name, 
                                        credential=self.credentials)
        return True
    def reset_db(self, config_data):
        self.search_index_client.delete_index(self.search_index_name)
        return True
    def store_vector_data(self, data):
        pass
    def do_vector_search(self, input_vector, app_config):
        pass
    def init_vector_storage(self,config_data):
        self.create_index(config_data)
        self.connect_to_vector_store()
        #TODO: Add error handling
        return True
    def get_fields_for_schema(self, schema, config_data):
        fields = []
        found_key = False
        found_vector = False
        vector_key = None
        for key in schema.keys():
            data = schema[key]
            if isinstance(data, str):
                field_type = Utils.parse_schema_string_value(data)
                if field_type == "GUID":
                    found_key = True
                    current_field = SimpleField(name=key, type=SearchFieldDataType.String, key=True)   
                    fields.append(current_field)
                else:
                    current_field = SearchableField(name=key, type=SearchFieldDataType.String)
                    fields.append(current_field)
            elif isinstance(data,list):
                found_vector = True
                vector_key = key
                current_field = SearchField(name=key, 
                                            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                                            searchable=True,
                                            vector_search_dimensions = config_data["vector_dimension"],
                                            vector_search_profile_name = config_data["vector_search_profile"])
                fields.append(current_field)
            elif isinstance(data,int):
                current_field = SimpleField(name=key, type=SearchFieldDataType.Int32)
                fields.append(current_field)
        if found_vector and found_key:
            return (fields, vector_key)
        
    def create_index(self, config_data):
        schema = self.data_schema  
        (fields, vector_key) = self.get_fields_for_schema(schema, config_data)
        self.vector_key = vector_key
        search_algo_config_name = config_data["vector_search_algorithm_configuration_name"]
        vector_search = VectorSearch(
            profiles=[VectorSearchProfile(name=config_data["vector_search_profile"], 
                                      algorithm_configuration_name=search_algo_config_name)],
            algorithms=[HnswAlgorithmConfiguration(name=search_algo_config_name)]
            )
        index = SearchIndex(name=self.search_index_name, fields=fields, vector_search=vector_search)
        self.search_index_client.create_index(index)
        #TODO: Add error handling
        return True
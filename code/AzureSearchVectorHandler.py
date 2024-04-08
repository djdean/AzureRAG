from VectorDBHandler import VectorDBHandler
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
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
import os
class AzureSearchVectorHandler(VectorDBHandler):
    def __init__(self, config_data):
        self.search_service_endpoint = config_data["search_service_endpoint"]
        self.search_service_key = config_data["search_service_key"]
        self.search_index_name = config_data["search_index_name"]
        self.credentials = AzureKeyCredential(self.search_service_key)
        self.search_index_client = SearchIndexClient(endpoint=self.search_service_endpoint, 
                                        index_name=self.search_index_name, 
                                        credential=self.credentials)
    def connect_to_index(self):
        self.client = SearchIndexClient(endpoint=self.search_service_endpoint, 
                                        index_name=self.search_index_name, 
                                        credential=self.credentials)
        return True
    def init_vector_storage(self,config_data):
        self.search_index_client.create_index(config_data)
        self.connect_to_index()
        #TODO: Add error handling
        return True
    def create_index(self, config_data):
        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SearchableField(name="content", type=SearchFieldDataType.String),
            SearchField(name="contentVector", 
                        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        searchable=True,
                        vector_search_dimension = config_data["vector_dimension"],
                        vector_search_profile = config_data["vector_search_profile"]
            ),
            SearchableField(name="company", type=SearchFieldDataType.String),
            SearchableField(name="model", type=SearchFieldDataType.String)
        ]
        search_algo_config_name = config_data["vector_search_algorithm_configuration_name"]
        vector_search = VectorSearch(
            profiles=[VectorSearchProfile(name=config_data["vector_search_profile"], 
                                      algorithm_configuration_name=search_algo_config_name)],
            algorithms=[HnswAlgorithmConfiguration(name=search_algo_config_name)]
            )
        index = SearchIndex(name=self.search_index_name, fields=fields, vector_fields=[vector_search])
        self.client.create_index(index)
        #TODO: Add error handling
        return True
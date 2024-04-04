from LLMHandler import LLMHandler
from openai import AzureOpenAI
class AOAIHandler(LLMHandler):
    def __init__(self, endpoint, api_key, api_version, temperature, model):
        self.client = AzureOpenAI(
            azure_endpoint = endpoint,
            api_key=api_key,
            api_version=api_version
        )
        self.model = model
        self.temperature = temperature
    def generate_embeddings(self, data):
        return self.client.embeddings.create(input = [data], model=self.model).data[0].embedding
    #TODO: Implement this method
    def get_response_from_model(self, data):
        pass

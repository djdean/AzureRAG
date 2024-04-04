import json
import tiktoken
class Utils:
    def __init__(self):
        pass
    def get_file_name_only(self, file_name):
        file_name_split = file_name.split("/")
        file_name_with_extension = file_name_split[len(file_name_split)-1]
        file_name_with_extension_split = file_name_with_extension.split(".")
        file_name_only = file_name_with_extension_split[0]
        return file_name_only
    
    def num_tokens_from_string(self, string: str, encoding_name: str) -> int:
        encoding = tiktoken.encoding_for_model(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens


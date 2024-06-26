from azure.storage.filedatalake import (
    DataLakeServiceClient,
    DataLakeDirectoryClient,
    FileSystemClient
)
class StorageHandler:
    def __init__(self, storage_account_name, storage_account_key, file_system_name=None):
        self.storage_account_name = storage_account_name
        self.storage_account_key = storage_account_key
        self.service_client = self.get_service_client_account_key(storage_account_name, storage_account_key)
        if file_system_name is not None:
            self.file_system_client = self.get_file_system_client(file_system_name)
        else:
            self.file_system_client = None
    def get_directories(self,path):
        paths = self.file_system_client.get_paths(path=path)
        return_paths = []
        for path in paths:
            if path.is_directory:
                return_paths.append(path.name)
        return return_paths
    def write_json_to_storage(self,output_name,output_data,directory_client):
        return_code = True
        try:
            file_client = directory_client.get_file_client(output_name)
            file_client.upload_data(output_data, overwrite=True)
        except Exception as e:
            return_code = False
        finally:
            return return_code
        
    def create_directory(self, directory_name: str) -> DataLakeDirectoryClient:
        directory_client = self.file_system_client.create_directory(directory_name)
        return directory_client
    
    def get_file_data(self, file_name,directory_client):
        file_client = directory_client.get_file_client(file_name)
        download = file_client.download_file()
        return download.readall()

    def get_file_system_client(self, file_system_name: str) -> FileSystemClient:
        file_system_client = self.service_client.get_file_system_client(file_system_name)
        return file_system_client

    def get_service_client_account_key(self, account_name, account_key) -> DataLakeServiceClient:
        account_url = f"https://{account_name}.dfs.core.windows.net"
        service_client = DataLakeServiceClient(account_url, credential=account_key)

        return service_client


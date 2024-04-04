from VectorDBHandler import VectorDBHandler
import urllib
import pymongo
class CosmosDBPyMongoVectorHandler(VectorDBHandler):

    def __init__(self, username, password, server):
        self.username = username
        self.password = password
        self.server = server
        self.mongo_conn = "mongodb+srv://"+urllib.parse.quote(self.username)+":"+urllib.parse.quote(self.password)+ \
        "@"+self.server+"?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
        self.mongo_client = pymongo.MongoClient(self.mongo_conn)

    def connect_to_vector_store(self, config_data):
        db_name = config_data["cosmos_db_name"]
        collection_name = config_data["cosmos_db_collection_name"]
        self.db = self.mongo_client[db_name]
        self.collection = self.db[collection_name]
        #TODO: Add error handling
        return True
    def reset_db(self, config_data):
        db_name = config_data["cosmos_db_name"]
        collection_name = config_data["cosmos_db_collection_name"]
        self.connect_to_vector_store(config_data)
        self.collection.drop_indexes()
        self.mongo_client.drop_database("DemoDB")
        #TODO: Add error handling
        return True
    def store_vector_data(self, data, settings):
        batch = settings["batch"]
        if batch:
            self.collection.insert_many(data)
        else:
            self.collection.insert_one(data)

    def do_vector_search(self, input_vector, settings):
        num_results = settings["num_results"]
        pipeline = [
            {
                '$search': {
                    "cosmosSearch": {
                        "vector": input_vector,
                        "path": "contentVector",
                        "k": num_results#, #, "efsearch": 40 # optional for HNSW only 
                        #"filter": {"title": {"$ne": "Azure Cosmos DB"}}
                    },
                    "returnStoredSource": True }}
        ]
        results = self.collection.aggregate(pipeline)
        return results
    
    def init_vector_storage(self,config_data):
        # create a database called TutorialDB
        db_name = config_data["cosmos_db_name"]
        collection_name = config_data["cosmos_db_collection_name"]
        vector_dimension = config_data["vector_dimension"]
        self.db = self.mongo_client[db_name]

        # Create collection if it doesn't exist
        COLLECTION_NAME = collection_name

        collection = self.db[COLLECTION_NAME]

        if COLLECTION_NAME not in self.db.list_collection_names():
            # Creates a unsharded collection that uses the DBs shared throughput
            self.db.create_collection(COLLECTION_NAME)
            print("Created collection '{}'.\n".format(COLLECTION_NAME))
        else:
            print("Using collection: '{}'.\n".format(COLLECTION_NAME))
        collection.drop_indexes()
        self.mongo_client.drop_database(db_name)
        self.db.command({
            'createIndexes': collection_name,
            'indexes': [
                {
                'name': 'VectorSearchIndex',
                'key': {
                    "contentVector": "cosmosSearch"
                },
                'cosmosSearchOptions': {
                    'kind': 'vector-ivf',
                    'numLists': 1,
                    'similarity': 'COS',
                    'dimensions': vector_dimension
                }
                }
            ]
            })
        self.collection = collection
        #TODO: Add error handling
        return True
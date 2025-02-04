from pymongo import MongoClient

class MongoDBManager:
    def __init__(self, db_name="IntentDB", uri="mongodb://localhost:27017"):
        """Instantiate MongoDB and create a database if it does not already exist."""
        self.client = MongoClient(uri)
        self.db_name = db_name
        db_list = self.client.list_database_names()
        if db_name not in db_list:
            self.db = self.client[db_name]
            print(f"Database '{db_name}' created and initialized.")
        else:
            self.db = self.client[db_name]
            print(f"Database '{db_name}' already exists. Using existing database.")

    def insert(self, collection_name: str, data: dict):
        """Insert a document into a collection."""
        collection = self.db[collection_name]
        collection.insert_one(data)
        print("Document inserted successfully.")

    def append(self, collection_name: str, query: dict, update_data: dict):
        """Append data to an existing document."""
        collection = self.db[collection_name]
        collection.update_one(query, {"$set": update_data}, upsert=True)
        print("Document updated successfully.")

    def remove(self, collection_name: str, query: dict):
        """Remove a document from a collection."""
        collection = self.db[collection_name]
        collection.delete_one(query)
        print("Document removed successfully.")

    def find(self, collection_name: str, query: dict):
        """Find a document in a collection."""
        collection = self.db[collection_name]
        return collection.find_one(query)
    
    def find_all(self, collection_name: str, query: dict):
        """Find all matching documents in a collection."""
        collection = self.db[collection_name]
        return list(collection.find(query))
    
    def clear_db(self):
        """Clear all collections in the database."""
        for collection_name in self.db.list_collection_names():
            self.db[collection_name].drop()
        print(f"All collections in database '{self.db_name}' have been cleared.")

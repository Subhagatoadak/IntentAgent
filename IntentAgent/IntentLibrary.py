import json
from MongoDBManager import MongoDBManager
import pandas as pd

class IntentLibrary:
    def __init__(self, db_manager: MongoDBManager, collection_name="Intents"):
        self.db_manager = db_manager
        self.collection_name = collection_name
        self.library = {}  # Dictionary to store hierarchy {domain: {intent: {sub-intents: [queries]}}}

    def add_intent(self, domain: str, intent_hierarchy: list, queries: list):
        """Check if the domain exists in MongoDB before adding an intent."""
        existing_domain = self.db_manager.find(self.collection_name, {"domain": domain})
        if not existing_domain:
            create_domain = input(f"Domain '{domain}' does not exist. Do you want to create it? (yes/no): ")
            if create_domain.lower() != "yes":
                return
            if len(queries) < 2:
                raise ValueError("A new domain must have at least one intent with at least two queries.")
            nested_intents = self.build_intent_structure(intent_hierarchy, queries)
            self.library[domain] = nested_intents
        else:
            existing_intents = existing_domain.get("intents", {})
            nested_intents = self.build_intent_structure(intent_hierarchy, queries)
            existing_intents = self.merge_dicts(existing_intents, nested_intents)
            self.library[domain] = existing_intents
        
        self.db_manager.append(self.collection_name, {"domain": domain}, {"intents": self.library[domain]})
        print(f"Intent '{' -> '.join(intent_hierarchy)}' added to domain '{domain}'.")
    
    def build_intent_structure(self, intent_hierarchy, queries):
        """Recursively build nested intent structure."""
        if len(intent_hierarchy) == 1:
            return {intent_hierarchy[0]: queries}
        return {intent_hierarchy[0]: self.build_intent_structure(intent_hierarchy[1:], queries)}
    
    def merge_dicts(self, dict1, dict2):
        """Recursively merge nested dictionaries."""
        for key, value in dict2.items():
            if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                dict1[key] = self.merge_dicts(dict1[key], value)
            else:
                dict1[key] = value
        return dict1
    
    def get_intents(self, domain: str, intent: str = None):
        """Retrieve intents based on domain and top-level intent."""
        query = {"domain": domain}
        result = self.db_manager.find(self.collection_name, query)
        if not result:
            return "No data found"
        
        intents = result.get("intents", {})
        if intent:
            return intents.get(intent, "Intent not found")
        return intents

    def remove_intent(self, domain: str, intent: str):
        """Check if the domain and intent exist before removing."""
        existing_domain = self.db_manager.find(self.collection_name, {"domain": domain})
        if not existing_domain:
            print("No such domain exists.")
            return
        
        if intent not in existing_domain.get("intents", {}):
            print("No such intent exists.")
            return
        
        del existing_domain["intents"][intent]
        self.db_manager.append(self.collection_name, {"domain": domain}, {"intents": existing_domain["intents"]})
        print(f"Intent '{intent}' removed from domain '{domain}'.")

    def remove_domain(self, domain: str):
        """Check if the domain exists before removing it."""
        existing_domain = self.db_manager.find(self.collection_name, {"domain": domain})
        if not existing_domain:
            print("No such domain exists.")
            return
        
        self.db_manager.remove(self.collection_name, {"domain": domain})
        print(f"Domain '{domain}' removed successfully.")
    
    def load_from_file(self, file_path: str):
        """Load data from an Excel, CSV, or SQL file into MongoDB with validations."""
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")
        
        for _, row in df.iterrows():
            domain = str(row.get("domain", "")).strip()
            intent_hierarchy = str(row.get("intent", "")).strip().split("->")
            queries = str(row.get("queries", "")).strip()
            
            if not domain or not intent_hierarchy or not queries:
                print("Skipping row due to empty domain, intent, or queries.")
                continue
            
            queries_list = queries.split(";")  # Assuming queries are separated by semicolons
            self.add_intent(domain, intent_hierarchy, queries_list)
        print("Data loaded successfully from file.")
    

import json
from MongoDBManager import MongoDBManager
import pandas as pd

class IntentLibrary:
    def __init__(self, db_manager: MongoDBManager, collection_name="Intents"):
        self.db_manager = db_manager
        self.collection_name = collection_name
        self.library = {}  # Dictionary to store hierarchy {domain: {intent: [queries]}}
        
    
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
            intent = str(row.get("intent", "")).strip()
            queries = str(row.get("queries", "")).strip()
            
            if not domain or not intent or not queries:
                print("Skipping row due to empty domain, intent, or queries.")
                continue
            
            queries_list = queries.split(";")  # Assuming queries are separated by semicolons
            
            existing_domain = self.db_manager.find(self.collection_name, {"domain": domain})
            if existing_domain:
                existing_intents = existing_domain.get("intents", {})
                if intent in existing_intents:
                    existing_intents[intent].extend(queries_list)
                else:
                    existing_intents[intent] = queries_list
                self.db_manager.append(self.collection_name, {"domain": domain}, {"intents": existing_intents})
            else:
                self.add_intent(domain, intent, queries_list)
        print("Data loaded successfully from file.")

    def add_intent(self, domain: str, intent: str, queries: list):
        """Check if the domain exists in MongoDB before adding an intent."""
        existing_domain = self.db_manager.find(self.collection_name, {"domain": domain})
        if not existing_domain:
            create_domain = input(f"Domain '{domain}' does not exist. Do you want to create it? (yes/no): ")
            if create_domain.lower() != "yes":
                return
            if len(queries) < 2:
                raise ValueError("A new domain must have at least one intent with at least two queries.")
            self.library[domain] = {intent: queries}
        else:
            existing_intents = existing_domain.get("intents", {})
            if intent in existing_intents:
                existing_intents[intent].extend(queries)
            else:
                existing_intents[intent] = queries
            self.library[domain] = existing_intents
        
        self.db_manager.append(self.collection_name, {"domain": domain}, {"intents": self.library[domain]})
        print(f"Intent '{intent}' added to domain '{domain}'.")

    def get_intents(self, domain: str = None, intent: str = None):
        """Retrieve intents based on domain or intent."""
        query = {}
        if domain:
            query["domain"] = domain
        
        results = self.db_manager.find_all(self.collection_name, query)
        
        if intent:
            filtered_results = []
            for result in results:
                if intent in result.get("intents", {}):
                    filtered_results.append({"domain": result["domain"], "intent": intent, "queries": result["intents"][intent]})
            return filtered_results
        
        return results
    
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

    def to_json(self):
        """Convert the library to JSON format."""
        return json.dumps(self.library, indent=4)



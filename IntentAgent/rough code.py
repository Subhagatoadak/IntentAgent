from MongoDBManager import MongoDBManager
from IntentLibrary import IntentLibrary

# Example usage
if __name__ == "__main__":
    db_manager = MongoDBManager()
    intent_lib = IntentLibrary(db_manager)
    intent_lib.add_intent("FMCG", ["buy_product", "electronics","Chcolate"], ["I want to buy a phone", "Purchase a laptop"])
    
    print("Retrieving intents by domain:")
    print(intent_lib.get_intents(domain="ecommerce"))
    
    print("Retrieving specific top-level intent:")
    print(intent_lib.get_intents(domain="FMCG", intent="buy_product"))

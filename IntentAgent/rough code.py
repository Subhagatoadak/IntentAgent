from mongodb import MongoDBManager
from IntentLibrary import IntentLibrary

if __name__ == "__main__":
    db_manager = MongoDBManager()
    intent_lib = IntentLibrary(db_manager)
    intent_lib.add_intent("ecommerce", "buy_product", ["I want to buy a phone", "Purchase a laptop"])
    intent_lib.add_intent("banking", "check_balance", ["What is my account balance?", "Show my balance"])
    print(intent_lib.to_json())
    
    print("Retrieving intents by domain:")
    print(intent_lib.get_intents(domain="ecommerce"))
    
    print("Retrieving specific intent:")
    print(intent_lib.get_intents(domain="ecommerce", intent="buy_product"))

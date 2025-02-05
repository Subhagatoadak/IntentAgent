from MongoDBManager import MongoDBManager
from IntentLibrary import IntentLibrary
from IntentAgent import IntentAgent

# Example usage
if __name__ == "__main__":
    db_manager = MongoDBManager()
    intent_lib = IntentLibrary(db_manager)
    intent_lib.add_intent("demo", ["buy_product", "electronics","Chcolate"], ["I want to buy a phone", "Purchase a laptop"])
    
    intent_lib.remove_domain("demo")
    intent_lib.remove_intent("ecommerce", "buy_product")
    
    print("Retrieving intents by domain:")
    print(intent_lib.get_intents(domain="ecommerce"))
    
    print("Retrieving specific top-level intent:")
    print(intent_lib.get_intents(domain="FMCG", intent="buy_product"))
    
    
    print(intent_lib.get_intents(domain="ecommerce"))
    agent = IntentAgent(intent_lib,None,'ecommerce')  # Intent library should be passed in real use cases
    print(agent.generate_prompt())
    agent.create_intent_methods("intent_methods.py")

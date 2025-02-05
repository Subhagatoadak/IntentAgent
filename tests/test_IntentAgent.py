import pytest
from IntentAgent import MongoDBManager
from IntentAgent import IntentLibrary
from IntentAgent import IntentAgent
from IntentAgent import LLMManager

@pytest.fixture
def db_manager():
    return MongoDBManager(db_name="TestIntentDB")

@pytest.fixture
def intent_library(db_manager):
    return IntentLibrary(db_manager)

@pytest.fixture
def llm_manager():
    return LLMManager(api_key="test_api_key", model_provider="openai")

@pytest.fixture
def intent_agent(intent_library, llm_manager):
    return IntentAgent(intent_library=intent_library, llm_manager=llm_manager)

def test_mongodb_insert_find(db_manager):
    sample_data = {"domain": "test_domain", "intents": {"test_intent": ["query1", "query2"]}}
    db_manager.insert("Intents", sample_data)
    result = db_manager.find("Intents", {"domain": "test_domain"})
    assert result is not None
    assert result["domain"] == "test_domain"
    assert "test_intent" in result["intents"]

def test_mongodb_append(db_manager):
    sample_data = {"domain": "test_domain", "intents": {"test_intent": ["query1"]}}
    db_manager.insert("Intents", sample_data)
    db_manager.append("Intents", {"domain": "test_domain"}, {"intents.test_intent": ["query2"]})
    result = db_manager.find("Intents", {"domain": "test_domain"})
    assert "query2" in result["intents"]["test_intent"]

def test_mongodb_remove(db_manager):
    sample_data = {"domain": "test_domain", "intents": {"test_intent": ["query1"]}}
    db_manager.insert("Intents", sample_data)
    db_manager.remove("Intents", {"domain": "test_domain"})
    result = db_manager.find("Intents", {"domain": "test_domain"})
    assert result is None

def test_create_intent_methods(intent_agent):
    test_intents = {
        "buy_product": {
            "electronics": {
                "phones": ["I want to buy a phone", "Purchase a mobile"]
            }
        }
    }
    intent_agent.intent_library.get_intents = lambda domain: test_intents
    intent_agent.create_intent_methods("ecommerce")
    
    with open("intent_methods.py", "r") as f:
        content = f.read()
    
    assert "def buy_product_electronics_phones()" in content

def test_llm_generate_response(llm_manager):
    prompt = "Test prompt for LLM"
    response = llm_manager.generate_response(prompt)
    assert isinstance(response, str)

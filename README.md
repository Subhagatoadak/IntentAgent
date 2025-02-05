
https://github.com/user-attachments/assets/14f1dde2-4d08-4db8-9f5b-dd2689abab78

# IntentAgent Library

This repository showcases a **modular library** for multi-level intent classification using MongoDB for storage and various LLM providers (OpenAI, Anthropic Claude, Google Gemini, Hugging Face) for classification. The system supports hierarchical intents (`domain -> intent -> subintent -> ...`) and generates dynamic Python methods for each intent.  

---

## Table of Contents

1. [Overview](#overview)  
2. [Project Structure](#project-structure)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Modules](#modules)  
   - [MongoDBManager](#mongodbmanager)  
   - [IntentLibrary](#intentlibrary)  
   - [LLMManager](#llmmanager)  
   - [IntentAgent](#intentagent)  
6. [Testing](#testing)  
7. [Environment and Dependencies](#environment-and-dependencies)  
8. [Contributing](#contributing)  
9. [License](#license)  

---

## Overview

- **Goal**: Classify user queries into hierarchical intents using a combination of:
  - **MongoDB** for domain-intent-query storage  
  - **LLM providers** for classification (OpenAI, Anthropic, Google Gemini, or Hugging Face)  
  - **Dynamic method generation** for each intent

- **Multi-level Intents**: The system supports nested intent structures, such as:

domain 
├─ intent 
└─ subintent1 
└─ subintent2 
└─ ...



- **Why MongoDB?**: Flexible schema lets you store hierarchical data for domains, intents, subintents, and queries without rigid table definitions.

- **Why LLMs?**: Large Language Models can interpret user queries, map them to existing hierarchical intents, and respond accordingly.

---

## Project Structure

An example layout could look like this:

├── mongodb_manager.py # MongoDBManager class 
├── intent_library.py # IntentLibrary class 
├── llm_manager.py # LLMManager class 
├── intent_agent.py # IntentAgent class 
├── test_intent_library.py # Pytest file for testing 
├── setup.py # Setup file for packaging 
├── requirements.txt # List of Python dependencies 
├── environment.yml # Conda environment definition 
└── intent_methods.py # (Auto-generated) dynamically created methods



---

## Installation

1. **Clone** this repository:
   ```bash
   git clone https://github.com/<your-username>/intentagent-library.git
   cd intentagent-library
   ```

Install dependencies:

```bash

pip install -r requirements.txt
```

or with conda:

```bash
conda env create -f environment.yml
conda activate intent-classification
```

(Optional) Install as a package:

```bash

python setup.py install
```
or

```bash

pip install .

```

Usage
Below is a quick example that demonstrates how these modules might be used together:

Initialize MongoDB and library classes:

```python

# main.py
from mongodb_manager import MongoDBManager
from intent_library import IntentLibrary
from llm_manager import LLMManager
from intent_agent import IntentAgent

# 1. Initialize MongoDB
db_manager = MongoDBManager(db_name="IntentDB", uri="mongodb://localhost:27017")

# 2. Create the IntentLibrary
intent_lib = IntentLibrary(db_manager)

# 3. Choose your LLM provider and API key
llm_manager = LLMManager(api_key="YOUR_API_KEY", model_provider="openai")

# 4. Create the IntentAgent
agent = IntentAgent(intent_library=intent_lib, llm_manager=llm_manager)
```


Add domain and intent (example usage, depending on your IntentLibrary methods):

```python

# Suppose your IntentLibrary has an add_intent method:
intent_lib.add_intent(
    domain="ecommerce",
    intent_hierarchy=["buy_product", "electronics", "phones"],
    queries=["I want to buy a phone", "Purchase a mobile"]
)
```

Generate a response:

```python

response = agent.get_llm_response("ecommerce")
print("LLM Response:", response)
# Response should be JSON with at least: {"intent": "buy_product", ...}
```
Create dynamic methods for the domain:

```python
agent.create_intent_methods("ecommerce")
# This writes a new file: intent_methods.py
# Example generated method: def buy_product_electronics_phones():
#   print("Executing buy_product_electronics_phones method.")
```

## Modules
**MongoDBManager**
File: mongodb_manager.py
Handles low-level MongoDB interactions:

insert(collection_name, data)
find(collection_name, query)
append(collection_name, query, update_data)
remove(collection_name, query)
find_all(collection_name, query)
clear_db()
Usage:

```python
db_manager = MongoDBManager(db_name="IntentDB", uri="mongodb://localhost:27017")
db_manager.insert("Intents", {"domain": "banking", "intents": {}})
```

**IntentLibrary**
File: intent_library.py
Manages domains, intents, subintents, and queries:

Add/Remove/Update domain and intents
Supports multi-level hierarchy
Uses db_manager to store and retrieve data in MongoDB
Usage:

```python
intent_library = IntentLibrary(db_manager)
intent_library.add_intent(
    domain="banking",
    intent_hierarchy=["check_balance"],
    queries=["What's my account balance?", "Show my balance"]
)
```

**LLMManager**
File: llm_manager.py
Connects to a specified LLM provider:

OpenAI (GPT-4, GPT-3.5, etc.)
Hugging Face
Anthropic (Claude)
Google Gemini
Implements:

```python
generate_response(prompt)
```

Usage:

```python
llm_manager = LLMManager(api_key="YOUR_API_KEY", model_provider="openai")
response = llm_manager.generate_response("Hello, world!")
print(response)
```

**IntentAgent**
File: intent_agent.py
Combines the IntentLibrary and LLMManager to:

Retrieve domain-based intents
Generate classification prompts for the LLM
Validate the LLM response in JSON (checking for at least "intent")
Create a Python file (intent_methods.py) with dynamically generated methods for each multi-level intent


**Key Methods**:

filter_intents(domain: str)
generate_prompt(domain: str)
get_llm_response(domain: str)
create_intent_methods(domain: str)


## Testing
We use pytest for testing. Test files are typically placed under a tests/ folder:

test_intent_library.py: Tests for the MongoDBManager, IntentLibrary, LLMManager, and IntentAgent.
Run tests:

```bash

pytest

```
If you’re using GitHub Actions, see the included CI workflow sample to run tests automatically (including integration with MongoDB as a service container).

## Environment and Dependencies


requirements.txt

pytest
pymongo
openai
anthropic
google-generativeai
transformers

environment.yml (for conda)
```yaml
name: intent-classification
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - pip
  - pip:
    - pymongo
    - openai
    - anthropic
    - google-generativeai
    - transformers
    - pytest
```

Use:

```bash
conda env create -f environment.yml
conda activate intent-classification
```
or:

```bash
pip install -r requirements.txt
```

## Contributing
   Fork the repository
   Create a feature branch
   Commit your changes
   Push to your branch
   Create a Pull Request
We welcome bug reports, feature requests, and improvements!

## License
Distributed under the MIT License (or your chosen license). See LICENSE for more information.






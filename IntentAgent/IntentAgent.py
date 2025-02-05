import json
from pydantic import BaseModel, ValidationError




class IntentAgent:
    def __init__(self, intent_library, llm_manager,domain):
        self.intent_library = intent_library
        self.llm_manager = llm_manager
        self.domain = domain
    
    def filter_intents(self):
        """Filter intents based only on domain."""
        intents = self.intent_library.get_intents(self.domain)
        return intents
    
    def generate_prompt(self):
        """Generate a more explicit prompt for multi-level intent classification."""
        intents = self.filter_intents()
        if not intents:
            return "No intents found for the given domain."
        
        def format_intents(intent_structure, level=0):
            formatted = ""
            for index, (intent, sub_intents) in enumerate(intent_structure.items()):
                intent_key = "intent" if level == 0 else f"subintent{level}"
                if isinstance(sub_intents, dict):
                    formatted += f"- {intent_key}: '{intent}'\n"
                    formatted += format_intents(sub_intents, level + 1)
                else:
                    examples = "; ".join(sub_intents)
                    formatted += f"- {intent_key}: '{intent}' with examples: [{examples}]\n"
            return formatted
        
        formatted_intents = format_intents(intents)
        
        prompt = (
            f"You are an expert AI assistant for the domain: '{self.domain}'.\n"
            f"Your task is to classify user queries into one of the predefined intents.\n"
            f"The intents in this domain can be multi-level, with hierarchical relationships.\n"
            f"Here are the intents and their corresponding example queries:\n{formatted_intents}\n"
            f"The output response from the LLM must be in JSON format with the following structure:\n"
            f"{{\n  'intent': '<top-level-intent>',\n  'subintent1': '<optional first-level sub-intent>',\n  'subintent2': '<optional second-level sub-intent>',\n  'subintentN': '<optional nested sub-intent>'\n}}\n"
            f"If no sub-intents exist, only the 'intent' field should be returned.\n"
            f"Now, classify the given user query accordingly."
        )
        return prompt
    
    def get_llm_response(self, domain: str):
        """Generate LLM response based on extracted intent information and validate JSON format."""
        prompt = self.generate_prompt(domain)
        response = self.llm_manager.generate_response(prompt)
        
        try:
            response_json = json.loads(response)
            if "intent" in response_json:
                return response_json
            else:
                raise ValueError("Response JSON is missing required key: 'intent'")
        except (json.JSONDecodeError, ValueError) as e:
            return {"error": "Invalid response format", "message": str(e)}
    
    def create_intent_methods(self,filename):
        """Dynamically create a Python file with methods for extracted intents."""
        intents = self.intent_library.get_intents(self.domain)
        file_content = """# Auto-generated intent methods\n\n"""
        
        def generate_method_name(intent_hierarchy):
            return "_".join(intent_hierarchy)
        
        def extract_methods(intent_structure, hierarchy=None):
            if hierarchy is None:
                hierarchy = []
            for intent, sub_intents in intent_structure.items():
                current_hierarchy = hierarchy + [intent]
                method_name = generate_method_name(current_hierarchy)
                if isinstance(sub_intents, dict):
                    extract_methods(sub_intents, current_hierarchy)
                else:
                    file_content_list.append(f"def {method_name}():\n    print(\"Executing {method_name} method.\")\n\n")
        
        file_content_list = []
        extract_methods(intents)
        file_content += "".join(file_content_list)
        
        with open(filename, "w") as f:
            f.write(file_content)
        print(f"Methods created for intents: {list(intents.keys())} in {filename}")

        


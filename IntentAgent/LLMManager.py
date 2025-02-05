import openai
import anthropic
import google.generativeai as genai
from transformers import pipeline


class LLMManager:
    def __init__(self, model_provider="openai", model="gpt-4", api_key=None):
        self.model_provider = model_provider
        self.model=model
        self.api_key = api_key
        
        if model_provider == "openai":
            self.client = openai.OpenAI(api_key=api_key)
        elif model_provider == "huggingface":
            self.hf_pipeline = pipeline("text-generation", model=self.model)
        elif model_provider == "claude":
            self.client = anthropic.Anthropic(api_key=api_key)
        elif model_provider == "gemini":
            genai.configure(api_key=api_key)
        else:
            raise ValueError("Unsupported LLM provider")

    def generate_response(self, prompt):
        if self.model_provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are an AI assistant."},
                          {"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        
        elif self.model_provider == "huggingface":
            response = self.hf_pipeline(prompt, max_length=200)[0]['generated_text']
            return response
        
        elif self.model_provider == "claude":
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        
        elif self.model_provider == "gemini":
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            return response.text
        
        else:
            raise ValueError("Unsupported LLM provider")
    
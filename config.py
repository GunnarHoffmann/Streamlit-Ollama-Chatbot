"""
Orignal Author: DevTechBytes
https://www.youtube.com/@DevTechBytes
"""

class Config:
    PAGE_TITLE = "Streamlit Ollama Chatbot"

    OLLAMA_MODELS = ('codellama:7b','deepseek-r1:14b')

    SYSTEM_PROMPT = f"""You are a helpful chatbot that has access to the following 
                    open-source models {OLLAMA_MODELS}.
                    You can can answer questions for users on any topic."""
    

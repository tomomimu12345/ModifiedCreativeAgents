from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted
import time

class ChatWrapper:
    def __init__(self, model_name, temperature=0.7, request_timeout=30):
        """
        ChatWrapper: Automatically selects backend based on model_name.
        
        Args:
            model_name (str): Model name to determine backend (e.g., "gpt-4", "gemini-2").
            temperature (float): Sampling temperature.
            request_timeout (int): Timeout for API requests.
            
        """
        self.model_name = model_name.lower()
        self.temperature = temperature
        self.request_timeout = request_timeout
        
        # Select backend based on model_name
        if self.model_name.startswith("gpt") or "openai" in self.model_name:
            self.backend = "openai"
            
            self.llm = ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                request_timeout=request_timeout,
            )
        elif self.model_name.startswith("gemini"):
            self.backend = "gemini"
            self.llm = ChatGoogleGenerativeAI(
                model = model_name,
                temperature=temperature,
                timeout=request_timeout,
            )
        else:
            raise ValueError(f"Unsupported model_name: {model_name}")

    def chat(self, messages):
        """
        Send messages to the selected backend.

        Args:
            messages (list[dict]): List of messages in the format [{"role": "user", "content": "..."}, ...]

        Returns:
           AI Message: {content:}
        """
        try:
            msg = self.llm.invoke(messages)
            msg.content = msg.content.replace("...", "")
            return msg

        except ResourceExhausted as e:
            # Handle rate limit error
            wait_time = 60  # Wait for 1 minute before retrying
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds.)")
            time.sleep(wait_time)
            return self.chat(messages)

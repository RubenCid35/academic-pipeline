from functools import lru_cache
from langchain_openai import ChatOpenAI

MODEL_VERSION: str = "gpt-4o"
MODEL_TEMPERATURE: float = 0.0

@lru_cache(maxsize=4)
def __get_llm() -> ChatOpenAI:
    """Loads and Instantiates a connection to the OpenAI model. 

    Returns:
        ChatOpenAI: model instance
    """
    model = ChatOpenAI(temperature=MODEL_TEMPERATURE, model_name = MODEL_VERSION)
    return model    
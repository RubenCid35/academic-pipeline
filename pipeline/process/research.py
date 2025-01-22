from pipeline.process.utils import __get_llm
from langgraph.graph import MessagesState

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from pydantic import BaseModel, Field

# ---------------------------------------------
# Metadata Format
# ---------------------------------------------
class ResearchInformation(BaseModel):
    research: list[str] = Field(description="list of key research findings")
    methodology: str = Field(description="description of the methodology that is described in the publication.")

parser = JsonOutputParser(pydantic_object=ResearchInformation)
# ---------------------------------------------
# Metadata Extraction
# ---------------------------------------------
RESEACH_EXTRACTION_TEMPLATE: str = """
Given the following academic publication content, you need to list all the key findings of the research and explain
the methodology that the authors used to discover them.. 

{format_instructions}

{content}
"""

RESEACH_EXTRACTION_PROMPT = PromptTemplate(
    template=RESEACH_EXTRACTION_TEMPLATE,
    input_variables = ["content"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)


def extract_research(state: dict[str, str]) -> dict[str, str]:
    """Research Information Extraction

    Using an LLM, this function extracts the methodology and key findings of a research publication.

    Args:
        state (dict[str, str]): state of the agent. It requires the field `content` with the pdf content as str.

    Returns:
        dict[str, str]: all metadata information and content.
    """
    # build processing steps
    llm   = __get_llm()
    chain = RESEACH_EXTRACTION_PROMPT | llm | parser

    # extract the required metadata
    research: dict[str, str] = chain.invoke({ 'content': state['content']})

    # add previous findings
    research.update(state)
    return research

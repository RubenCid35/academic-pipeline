from pipeline.process.utils import __get_llm
from langgraph.graph import MessagesState

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from pydantic import BaseModel, Field
from datetime import datetime
# ---------------------------------------------
# Metadata Format
# ---------------------------------------------
class Metadata(BaseModel):
    title: str = Field(description="title of the academic publication")
    authors: list[str] = Field(description="list of authors of the publication")
    abstract: str  = Field(description="abstract text of the academic publication")
    publication_date: datetime = Field(description="publication date of the publication to be parsed")

parser = JsonOutputParser(pydantic_object=Metadata)
# ---------------------------------------------
# Metadata Extraction
# ---------------------------------------------
METADATA_TEMPLATE: str = """
Given the following academic publication content, retrieve the title, authors names, abstract text and publication date.
If any of the fields is missing, please return "none". 

{format_instructions}

{content}
"""

METADATA_PROMPT = PromptTemplate(
    template=METADATA_TEMPLATE,
    input_variables = ["content"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)


def extract_metadata(state: dict[str, str]) -> dict[str, str]:
    """Metadata Extraction

    Using an LLM (gpt-01-mini), we extract the following metadata:
    * Authors
    * Title
    * Abstract
    * Publication Date

    Args:
        state (dict[str, str]): pdf content as a string

    Returns:
        dict[str, str]: metadata dictionary
    """
    # build processing steps
    llm   = __get_llm()
    chain = METADATA_PROMPT | llm | parser

    # extract the required metadata
    metadata = chain.invoke(state)

    # extract date from datetime. The output is a datetime as string. 
    metadata['publication_date'] = metadata['publication_date'].split("T", 2)[0]

    # modify author
    metadata['authors'] = [ {'name': name } for name in metadata['authors'] ]

    # persist the file content for future steps
    metadata.update(state)
    return metadata

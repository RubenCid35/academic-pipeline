from pipeline.process.utils import __get_llm
from langchain_core.prompts import PromptTemplate
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.utils import get_buffer_string
# ---------------------------------------------
# Metadata Extraction
# ---------------------------------------------
SUMMARY_TEMPLATE: str = """
Write a concise summary with the main information of the following academic publication:

{content}
"""

SUMMARY_PROMPT = PromptTemplate(
    template=SUMMARY_TEMPLATE,
    input_variables = ["content"],
)


def summarize_paper(state: dict[str, str]) -> dict[str, str]:
    """Summarize the paper content using an gpt-3.5. 

    Args:
        state (dict[str, str]): state of the agent. It requires the field `content` with the pdf content as str.

    Returns:
        dict[str, str]: state with a new `summary` field.
    """
    # build processing steps
    llm   = __get_llm()
    chain = SUMMARY_PROMPT | llm 

    # generate the summary using raw text
    summary: AIMessage = chain.invoke({ 'content': state['content']})

    # add summary to the code
    state['summary'] = summary.content
    return state

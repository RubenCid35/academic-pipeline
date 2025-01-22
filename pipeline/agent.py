from typing import TypedDict, Literal

from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage

# instantiate the workflow
pipeline_flow = StateGraph(BaseMessage, config_schema={})

# add the workflow steps

# Compile the graph
graph = pipeline_flow.compile()
from typing import TypedDict, Literal

from fastapi   import FastAPI
from langserve import add_routes

from io import BytesIO

from langgraph.graph import StateGraph, START, END, Graph
from langchain_core.messages import BaseMessage

# graph nodes
from pipeline.process.ingestion import ingest_pdf
from pipeline.process.metadata  import extract_metadata

# instantiate the workflow
pipeline_flow = Graph()

# add the workflow steps
pipeline_flow.add_node('ingestion', ingest_pdf)
pipeline_flow.add_node('metadata-extraction', extract_metadata)

# order steps
pipeline_flow.add_edge(START, 'ingestion')
pipeline_flow.add_edge('ingestion', 'metadata-extraction')
pipeline_flow.add_edge('metadata-extraction', END)

# Compile the graph
graph = pipeline_flow.compile()
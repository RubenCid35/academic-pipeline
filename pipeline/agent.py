from langgraph.graph import Graph
from langgraph.graph import START, END
from langchain_core.messages import BaseMessage

# graph nodes
from pipeline.process.ingestion import ingest_pdf
from pipeline.process.metadata  import extract_metadata
from pipeline.process.research  import extract_research
from pipeline.process.summary   import summarize_paper

# instantiate the workflow
pipeline_flow = Graph(dict)

# add the workflow steps
pipeline_flow.add_node('ingestion', ingest_pdf)
pipeline_flow.add_node('metadata-extraction', extract_metadata)
pipeline_flow.add_node('research-extraction', extract_research)
pipeline_flow.add_node('summarization', summarize_paper)

# order steps
# all steps are done sequentialy
pipeline_flow.add_edge(START, 'ingestion')
pipeline_flow.add_edge('ingestion', 'metadata-extraction')
pipeline_flow.add_edge('metadata-extraction', 'research-extraction')
pipeline_flow.add_edge('research-extraction', 'summarization')
pipeline_flow.add_edge('summarization', END)

# Compile the graph
graph = pipeline_flow.compile()
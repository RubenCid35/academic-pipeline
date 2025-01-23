from langgraph.graph import Graph
from langgraph.graph import START, END
from langchain_core.messages import BaseMessage

# graph nodes
from pipeline.process.ingestion import ingest_pdf
from pipeline.process.metadata  import extract_metadata
from pipeline.process.research  import extract_research
from pipeline.process.summary   import summarize_paper
from pipeline.process.load      import load_results_bigquery

from pipeline.process.verify    import validate_metadata

# instantiate the workflow
pipeline_flow = Graph()

# add the workflow steps
pipeline_flow.add_node('ingestion', ingest_pdf)
pipeline_flow.add_node('metadata-extraction', extract_metadata)
pipeline_flow.add_node('research-extraction', extract_research)
pipeline_flow.add_node('summarization', summarize_paper)
pipeline_flow.add_node('upload-results', load_results_bigquery)

# validation steps
pipeline_flow.add_node('metadata-validation', validate_metadata)

# order steps
# all steps are done sequentialy
pipeline_flow.add_edge(START, 'ingestion')
pipeline_flow.add_edge('ingestion', 'metadata-extraction')
pipeline_flow.add_edge('metadata-extraction', 'metadata-validation')
pipeline_flow.add_edge('metadata-validation', 'research-extraction')
pipeline_flow.add_edge('research-extraction', 'summarization')
pipeline_flow.add_edge('summarization', 'upload-results')
pipeline_flow.add_edge('upload-results', END)

# Compile the graph
graph = pipeline_flow.compile()
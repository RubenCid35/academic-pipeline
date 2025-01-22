from typing  import Annotated 

# load environment file
import dotenv
dotenv.load_dotenv()

import uvicorn
from fastapi import FastAPI, File

from pipeline.agent import graph
from langchain_core.runnables import RunnableConfig


# Initialize the endpoints
app = FastAPI()

@app.post('/process')
async def process(file: Annotated[bytes, File()]):
    """Processing Endpoint

    Args:
        file (Annotated[bytes, File): PDF file to process

    Returns:
        dict[str, any]: JSON with some metadata
    """
    input_data = { 'file': file }
    content = await graph.ainvoke(input_data)
    return content


if __name__ == '__main__':
    uvicorn.run(".:app", host = "localhost", port = 4321, reload = False)
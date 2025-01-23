from typing  import Annotated 

# load environment file
import dotenv
dotenv.load_dotenv()

import uvicorn
from fastapi import FastAPI, File

from pipeline.agent import graph
from pipeline.logging import logger


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
    try:
        content = await graph.ainvoke(input_data)
    except ValueError:
        logger.error("metadata / research validation steps failed.")
        content = False
    return content


if __name__ == '__main__':
    # deploy settings for google cloud run
    uvicorn.run(app, host="0.0.0.0", port=80)
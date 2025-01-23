from typing import Annotated
from pipeline.logging import logger

# Load environment file
import dotenv
dotenv.load_dotenv()

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, status

from pipeline.agent import graph
import magic  # For file type validation


# Initialize the endpoints
app = FastAPI()

@app.post('/process')
async def process(file: Annotated[UploadFile, File()]):
    """Processing Endpoint

    Args:
        file (Annotated[UploadFile, File]): PDF file to process

    Returns:
        dict[str, any]: JSON with some metadata
    """
    # Validate file type
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(await file.read(1024))
    if file_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF files are allowed."
        )
    
    # Reset file pointer after validation
    file.file.seek(0)

    input_data = {'file': file.file.read()}
    try:
        content = await graph.ainvoke(input_data)
    except ValueError as e:
        logger.error(f"Processing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during processing. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
    
    return {"status": "success", "content": content}


if __name__ == '__main__':
    # Deploy settings for Google Cloud Run
    uvicorn.run(app, host="127.0.0.1", port=8080)

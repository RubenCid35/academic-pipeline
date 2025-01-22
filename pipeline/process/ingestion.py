
import logging
from io import BytesIO
from typing import Any

from langchain.schema import Document
from langgraph.graph import MessagesState

from langchain_core.document_loaders import Blob
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders.parsers.pdf import PyMuPDFParser

# ---------------------------------------------
# Custom PDF Loader 
# ---------------------------------------------
# THe main pdf laoders assume the file is locally downlaoded and
# they dont allow to parse byte-objects pdf.
# Following code is from: https://github.com/langchain-ai/langchain/pull/6268
class BytesIOPyMuPDFLoader(PyMuPDFLoader):
    """Load `PDF` files using `PyMuPDF` from a BytesIO stream."""

    def __init__(
        self,
        pdf_stream: BytesIO,
        *,
        extract_images: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize with a BytesIO stream."""
        self.pdf_stream = pdf_stream
        self.extract_images = extract_images
        self.text_kwargs = kwargs

    def load(self, **kwargs: Any) -> list[Document]:
        """Load file."""
        if kwargs:
            logging.warning(
                f"Received runtime arguments {kwargs}. Passing runtime args to `load`"
                f" is deprecated. Please pass arguments during initialization instead."
            )

        text_kwargs = {**self.text_kwargs, **kwargs}

        # Use 'stream' as a placeholder for file_path since we're working with a stream.
        blob = Blob.from_data(self.pdf_stream.getvalue(), path="stream")
        parser = PyMuPDFParser(
            text_kwargs=text_kwargs, extract_images=self.extract_images
        )

        return parser.parse(blob)

# ---------------------------------------------
# PDF Ingestion Node
# ---------------------------------------------
def ingest_pdf(state: MessagesState) -> str:
    """Ingestion of PDF File. 
    
    This method is oriented for cloud file uploads where the file is not downloaded in the machine.
    The content of the pdf are parsed and joined in one unique literal string. Most of the academic
    publications contain few pages. 

    Args:
        state (MessagesState): state of agent. It will contain the file
        config (RunnableConfig): configuration. It is not used.

    Returns:
        str: file content as one text.
    """
    # get file input as bytes
    pdf_stream  = BytesIO(state['file'])
    
    # read pdf text content 
    pdf_reader  = BytesIOPyMuPDFLoader(pdf_stream, extract_images=False)
    
    # parse and join all content
    pdf_content = pdf_reader.load()
    pdf_content = ''.join([page.page_content.replace('\t', ' ') for page in pdf_content])
    return { 'content': pdf_content }
    

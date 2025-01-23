import os

from pipeline.logging import logger

from google.cloud import bigquery
from google.oauth2.service_account import Credentials

# determine the table where the data is going to be uploaded
BIGQUERY_DATASET_ID: str = os.environ.get("BIQUERY_DATASET")
BIGQUERY_TABLE: str = os.environ.get("BIQUERY_TABLE")

# create connection to bigquery client
credentials_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
credentials = Credentials.from_service_account_file(credentials_file)
client = bigquery.Client(BIGQUERY_DATASET_ID.split(".")[0], credentials)

def load_results_bigquery(state: dict[str, str]):
    """
    Load the results into BigQuery.

    Args:
        state (dict[str, str]): A dictionary containing the data to be uploaded to BigQuery.
    
    Returns:
        bool: True if the data is uploaded successfully, False otherwise.
    """
    logger.info("Started loading results to BigQuery.")

    # Remove the 'content' field to avoid clutter in the database
    if 'content' in state: del state['content']

    # Insert the rows into the database
    try:
        errors = client.insert_rows_json(BIGQUERY_TABLE, [state])

        if not errors: return True # end without issue
        else:
            logger.error(f"Failed to insert rows into BigQuery: {errors}")
            return False
    except Exception as error:
        logger.exception(f"An error occurred while uploading to BigQuery: {error}")
        return False
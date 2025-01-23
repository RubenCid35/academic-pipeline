# list of conditional steps
# this steps are used to verify
# - pdf is not empty
# - title, abstract, authors are found (publication date can be missing, many papers dont include it)
# https://sensia.jobs.personio.de/job/1335662?language=en&display=en#apply

from pipeline.logging import logging

def validate_metadata(state: dict[str, str]) -> dict[str, str]:
    """Validate the results of the metadata extraction. As some publications may not contain the 
    publication date, this validation step only tries to check if the following fields or data 
    points were found and filled: 
    * title
    * abstract
    * authors (it checks if we find at least one author)

    Args:
        state (dict[str, str]): metadata information. 

    Raises:
        ValueError: title was not found
        ValueError: abstract text was not found
        ValueError: not authors were found

    Returns:
        dict[str, str]: original state
    """

    if 'title' not in state and state['title'] == "":
        logging.error(f"file {state['id']}: title field was not found")
        raise ValueError(f"title was not found in academic paper ({state['id']})")
    
    if 'abstract' not in state and state['abstract'] == "":
            logging.error(f"file {state['id']}: abstract text was not found")
            raise ValueError(f"abstract text was not found in academic paper ({state['id']})")

    if 'authors' not in state and state['authors'] == []:
            logging.error(f"file {state['id']}: no authors were identified in the publication")
            raise ValueError(f"no authors were identified in paper ({state['id']})")

    return state
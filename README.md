# Coding Challenge: Astrafy

## Description

This repository contains the implementation of a LangChain-based data pipeline designed for processing academic publications. It operates via a REST API endpoint, which accepts raw PDF files, processes them, and uploads the results to a BigQuery table. The API endpoint is `/process`.

The processing pipeline consists of the following steps:

1. File Ingestion: The raw PDF file is uploaded and prepared for processing.
2. Metadata Extraction: Extracts key information such as the title, abstract, authors, and publication date.
3. Metadata Verification: Verifies the presence of the extracted metadata. If any required metadata is missing, the process is terminated.
4. Research Information Extraction: Generates summaries of the publication's findings and methodology to enable further comparison.
5. General Summary: Produces a high-level summary of the publication for broader context.
6. BigQuery Upload: Uploads the processed results to the designated BigQuery table for storage and analysis.

## Code Structure

This repository contains two modules or components: the data pipeline and a rudimentary interface
for individual uploads. 

### Data Pipeline
The data pipeline code is structured as follows:

* `service.py`: Deploys and runs the data pipeline endpoint.
* `pipeline/`:  Contains the general data pipeline module, including all relevant code.
    * `pipeline/agent.py`: Contains the code to create the LangChain agent and orchestrate all the pipeline steps.
    * `pipeline/process/`: Contains the implementation of individual steps for the extraction blocks. Each step is treated as a separate module for modularity and flexibility.
    * `pipeline/logging.py`:Implements general logging functionality for the pipeline.
* `requirements-pipeline.txt`: Specifies the Python libraries required for running the pipeline.
* `Dockerfile`: Contains the configuration for Docker deployment. This file requires modifications before use (details provided later under Deployment).

### Interface
The interface module contains:

* `interface.py`: The code for the rudimentary interface to handle individual uploads.
* `requirements-interface.txt`: Specifies the Python libraries required for running the interface.

## Execution Steps
### Prerequisites

Before proceeding with the deployment and execution, you will be required to obtain:
* OpenAI Key: The pipeline uses GPT-3.5 for text generation. Ensure you have a valid OpenAI API key.
* `key.json`: A file containing the credentials needed to access BigQuery. 
* BigQuery Table ID: id of the table were the results will be uploaded.

To obtain the required credentials, you need to perform the following steps:
1. Set up a Google Cloud Project
2. Create a BigQuery dataset and table withing the project. The table needs to follow the schema from `bigquery-table.json`. Copy the id of the table, it is required later. 
3. Go to "IAM & Admin" > "Service Accounts". Create a service account with the role "BigQuery Data Editor" and generate the a credentials file for that account.

### Pipeline: Local Execution
To run the pipeline locally, follow these steps:

1. Create an `.env` file:
    Add the necessary configuration information to a file named `.env` in the root directory. Populate it with the following content, replacing placeholders with the appropriate values:

```bash
OPENAI_API_KEY=<OPENAI KEY>
GOOGLE_APPLICATION_CREDENTIALS="./key.json"
BIQUERY_TABLE=<TABLE ID>
```
2. Install Dependencies
    Install all the required libraries using the provided requirements file:
```bash
pip install -r requirements-pipeline.txt
```
3. Run the Pipeline
    Start the pipeline service using uvicorn:
```bash
uvicorn service:app --host localhost --port 4321
```

### Pipeline: Docker Execution
To run the pipeline using Docker, follow these steps:

1. Create an `.env` file:
    Add the necessary configuration information to a file named `.env` in the root directory. Populate it with the following content, replacing placeholders with the appropriate values:

```bash
OPENAI_API_KEY=<OPENAI KEY>
GOOGLE_APPLICATION_CREDENTIALS="./key.json"
BIQUERY_TABLE=<TABLE ID>
```
2. Build the Docker Image:
    Build the Docker image using the following command:
```bash
docker build -t astrafy-pipeline . 
```
3. Build the Docker Image:
    Run the Docker container while mapping the appropriate port:
```bash
docker build -t astrafy-pipeline . 
```

### Pipeline: Google Cloud Deployment

To deploy the pipeline using Google Cloud, follow these steps from google cloud shell.
1. Clone the repository:
    Start by cloning the repository and navigating into the project directory:
```bash
git clone https://github.com/RubenCid35/academic-pipeline
cd academic-pipeline
```
2. Set Up a Service Account and Generate `key.json`
    Create a service account with the required permissions for BigQuery and Cloud Build:
```bash
gcloud iam service-accounts create bigquery-pipe-sa --display-name "Bigquery Academic Librarian"
gcloud iam service-accounts keys create ~/key.json --iam-account bigquery-pipe-sa@${PROJECT_ID}.iam.gserviceaccount.com
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:bigquery-pipe-sa@${PROJECT_ID}.iam.gserviceaccount.com"
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:bigquery-pipe-sa@${PROJECT_ID}.iam.gserviceaccount.com" 
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:bigquery-pipe-sa@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/bigquery.user"
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:bigquery-pipe-sa@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/bigquery.editor"
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:bigquery-pipe-sa@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/bigquery.dataEditor"
gcloud services enable cloudbuild.googleapis.com
```
3. Create an `.env` file:
    Add the necessary configuration information to a file named `.env` in the root directory. Populate it with the following content, replacing placeholders with the appropriate values:

```bash
OPENAI_API_KEY=<OPENAI KEY>
GOOGLE_APPLICATION_CREDENTIALS="./key.json"
BIQUERY_TABLE=<TABLE ID>
```
4. Build the Docker Image
    Use Cloud Build to create and push a Docker image for your pipeline:
```bash
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/data-pipeline:1.0.0 .
```
5. Deploy to Google Cloud Run
Deploy the pipeline to Cloud Run in your preferred region. The terminal will ask to input the desired region.
```bash
gcloud run deploy --image=gcr.io/${GOOGLE_CLOUD_PROJECT}/data-pipeline:1.0.0 --platform managed --allow-unauthenticated
```
6. Test the Deployment
You can use PostMan or the pre-made interface to test the deployment.

### Interface:
The interface is intented to be run only in a local setup. This interface runs on the browser and allows to send an academic publication to the pipeline.
These steps are required to run the interface:
```bash
pip install -r requirements-interface.txt
streamlit run interface.py
```
You will be required to add the pipeline url at the start of the interface.


## Limitations

While the pipeline effectively processes academic publications, there are a few limitations to keep in mind:

* **Duplicate Results**
    The pipeline does not check for uniqueness in the processed results. If the same file is uploaded multiple times, duplicate entries may be created in the BigQuery table. The individual ids will be different.

* **Performance**
    The pipeline requires an average of 10 seconds to extract and parse all information from a single file.
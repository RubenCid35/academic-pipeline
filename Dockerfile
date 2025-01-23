# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements-pipeline.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements-pipeline.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME=LangChainService

# Run the application
ENTRYPOINT [ "python" ]
CMD ["service.py"]
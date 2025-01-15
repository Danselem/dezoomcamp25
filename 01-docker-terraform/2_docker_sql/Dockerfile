FROM python:3.10.1-slim

# Update package lists and install wget
RUN apt-get update && apt-get install -y wget

# Install Python dependencies
RUN pip install pandas sqlalchemy psycopg2-binary

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY ingest_data.py ingest_data.py 

# Define the entry point for the container
ENTRYPOINT [ "python", "ingest_data.py" ]
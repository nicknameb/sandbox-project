FROM ubuntu:22.04
CMD "bash" 

# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the local script to the container
COPY sandbox_script.py /app/sandbox_script.py

# Install necessary Python packages
# If you have additional dependencies, list them in a requirements.txt file
RUN pip install docker
RUN apt-get update && apt-get install -y clamav
# Define the default command to execute your script
CMD ["python", "sandbox_script.py"]

# Use the official Python image as a base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ../requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY .. .

# Set environment variables (if needed)
# ENV VARIABLE_NAME value

# Expose the port your app runs on
EXPOSE 5000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
FROM ubuntu:latest
LABEL authors="samitsega"

ENTRYPOINT ["top", "-b"]
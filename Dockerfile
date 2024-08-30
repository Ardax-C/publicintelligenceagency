# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask and Werkzeug with specific versions
RUN pip install --no-cache-dir Flask==2.0.1 Werkzeug==2.0.1

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables
ENV NAME PublicIntelligenceAgency
ENV PYTHONPATH=/app

# Run app.py when the container launches
CMD ["python", "search/search_interface.py"]
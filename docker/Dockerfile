# Use Python 3.11 slim as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the python code into the container
COPY source .

# Set the default command to run mr_plot.py
ENTRYPOINT ["python", "mr_plot.py"]

# Default arguments (can be overridden at runtime)
CMD ["--help"]


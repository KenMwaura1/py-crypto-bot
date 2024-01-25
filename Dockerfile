# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot_2.py file to the working directory
COPY bot_2.py .

# Run the bot_2.py script
CMD ["python", "bot_2.py"]

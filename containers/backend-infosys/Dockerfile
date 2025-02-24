# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the app
EXPOSE 5000

# Run app.py when the container starts
CMD ["python", "app.py"]

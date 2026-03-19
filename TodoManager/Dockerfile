# Use official lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
# We do this before copying the rest of the app to cache the layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app into the container (except what's in .dockerignore)
COPY . .

# Expose port 5000 for the Flask/Gunicorn server
EXPOSE 5000

# Start Gunicorn, binding to 0.0.0.0:5000 and pointing to app:app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

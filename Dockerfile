# Base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose the port
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]

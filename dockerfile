FROM python:3.11.9

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && apt-get clean

# Copy the current directory contents into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000
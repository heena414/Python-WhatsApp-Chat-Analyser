# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Ensure that Python outputs everything to the console without buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for common Python libraries (fixing build failure due to missing dependencies)
# - 'apt-get update' updates the package list
# - 'build-essential' includes necessary tools like 'gcc' for compiling certain Python dependencies
# - 'libpq-dev' might be necessary for PostgreSQL integrations (adjust based on your project)
# - 'curl' for downloading files if needed during builds
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker layer caching
COPY rerequirements.txt /app/

# Install dependencies with pip using --root-user-action=ignore to avoid permission issues
# This command upgrades pip and then installs the dependencies while suppressing the warning
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --root-user-action=ignore -r rerequirements.txt

# Copy the rest of the application source code
COPY . /app

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run Streamlit when the container launches
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]




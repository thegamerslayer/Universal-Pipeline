# Use a slim Python base
FROM python:3.12-slim

# Install system dependencies if needed (none for now)
# RUN apt-get update && apt-get install -y --no-install-recommends ...

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set PYTHONPATH so 'app.core' and 'app.stages' are discoverable
ENV PYTHONPATH=/app

# Create a data directory for output
RUN mkdir -p /app/data

# Default command: Run the pipeline
# The user can override this in docker-compose for the notebook service
CMD ["python", "app/main.py"]
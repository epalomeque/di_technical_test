# Use official Python 3.11 image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies for building psycopg2 and other libs
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Create and prepare virtualenv
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip
ENV PATH="/venv/bin:${PATH}"


# Install Python dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y build-essential libpq-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Expose Django port
EXPOSE 8000

# Default command (can be overridden by docker-compose)
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]


FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Accept build arguments from OS environment
ARG SECRET_KEY
ARG DEBUG
ARG ALLOWED_HOSTS
ARG CSRF_TRUSTED_ORIGINS
ARG POSTGRES_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_HOST
ARG POSTGRES_PORT

# Set environment variables from build arguments
ENV SECRET_KEY=$SECRET_KEY
ENV DEBUG=$DEBUG
ENV ALLOWED_HOSTS=$ALLOWED_HOSTS
ENV CSRF_TRUSTED_ORIGINS=$CSRF_TRUSTED_ORIGINS
ENV POSTGRES_DB=$POSTGRES_DB
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_HOST=$POSTGRES_HOST
ENV POSTGRES_PORT=$POSTGRES_PORT

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Create entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["uv", "run", "python", "main.py", "runserver", "0.0.0.0:8000"]


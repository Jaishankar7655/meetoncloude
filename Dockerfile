# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update \
    && apt-get install -y \
        default-libmysqlclient-dev \
        pkg-config \
        gcc \
        g++ \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install mysqlclient
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Install only runtime dependencies (no build tools)
RUN apt-get update \
    && apt-get install -y \
        default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . /app/

EXPOSE 8000
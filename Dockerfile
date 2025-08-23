# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
FROM python:3.11-slim

# Add user that will be used in the container.
RUN useradd -m wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/srcs

# Install system packages required by Wagtail and Django
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# Install the application server
RUN pip install --no-cache-dir gunicorn

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir .

# Create necessary directories and set permissions
RUN mkdir -p /app/data /app/static /app/media && \
    chown -R wagtail:wagtail /app

# Use user "wagtail" to run the server itself.
USER wagtail

# Collect static files.
RUN python srcs/manage.py collectstatic --noinput

# 스크립트에 실행 권한 부여
RUN chmod +x /app/srcs/config/db/init.sh

CMD ["python", "srcs/manage.py", "runserver", "0.0.0.0:8000"]

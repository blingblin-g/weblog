# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
FROM python:3.12-slim-bookworm

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
    NODE_ENV=production \
    PYTHONPATH=/app/srcs

# Install system packages required by Wagtail, Django, and Node.js
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

# Install the application server and uv
RUN pip install --no-cache-dir gunicorn uv

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN uv pip install --system .

# Install Node.js dependencies and build Tailwind CSS (root 권한)
WORKDIR /app/srcs/theme
RUN npm install && npm run build

# Go back to app directory
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. (빌드 후 소유권 변경)
RUN chown -R wagtail:wagtail /app

# Use user "wagtail" to run the server itself.
USER wagtail

# Collect static files.
RUN python srcs/manage.py collectstatic --noinput

# 스크립트에 실행 권한 부여
RUN chmod +x /app/srcs/config/db/init.sh

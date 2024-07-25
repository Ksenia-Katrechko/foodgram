# Pull base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# installing and upgrading tools
RUN apt-get update && apt-get install -y --no-install-recommends make curl \
    && apt-get install nano && apt-get install vim -y  \
    && apt-get clean \
    && pip install --upgrade pip

# Install dependencies
COPY backend/requirements.txt .

RUN pip install -r requirements.txt

# Copy project
COPY backend/ .

# Collect static files
RUN python manage.py collectstatic --noinput

# Start server
CMD ["gunicorn", "--bind", "0.0.0.0:7000", "foodgram.wsgi:application"]
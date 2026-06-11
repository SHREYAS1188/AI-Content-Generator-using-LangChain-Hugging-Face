# Basic Dockerfile for running the FastAPI app in production
# Use slim Python image and create a non-root user

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Use unprivileged user
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup
USER appuser

ENV PYTHONPATH=/app/src
EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]


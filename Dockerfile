# Railway deployment Dockerfile for Pydantic Model Generator
# Handles monorepo structure by copying pydantic_library into backend

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy pydantic_library first (needed by backend)
COPY pydantic_library ./pydantic_library

# Copy backend application
COPY backend ./backend

# Install Python dependencies
WORKDIR /app/backend
RUN pip install --no-cache-dir -r requirements.txt

# Copy pydantic_library into backend for runtime access
RUN cp -r /app/pydantic_library ./pydantic_library

# Expose port (Railway assigns $PORT dynamically)
EXPOSE 8000

# Start command
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

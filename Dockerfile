# Base Image
FROM python:3.11-slim

# Set Working Directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project Files
COPY . .

# Expose Port
EXPOSE 8000

# Run FastAPI Application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
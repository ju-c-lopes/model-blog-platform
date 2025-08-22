FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/website:/app/blogModel

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies at runtime (commented out due to network issues)
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["tail", "-f", "/dev/null"]

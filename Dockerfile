FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install Python dependencies at runtime (commented out due to network issues)
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --no-interaction --no-ansi

ENV PATH="/app/.venv/bin/:$PATH"

ENV PYTHONPATH=/app

COPY . /app/

# Default command
CMD ["tail", "-f", "/dev/null", "&&", "poetry", "env", "activate", "&&", "poetry", "install"]

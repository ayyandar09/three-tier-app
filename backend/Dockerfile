FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Update OS packages and install Python dependencies
COPY requirements.txt .

RUN apt-get update \
    && apt-get upgrade -y \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY app ./app

# Create non-root application user
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --uid 10001 appuser \
    && chown -R 10001:10001 /app

USER 10001

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
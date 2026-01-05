FROM python:3.11-slim

WORKDIR /app

COPY app.py /app

RUN pip install \
    fastapi uvicorn \
    opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-instrumentation-fastapi \
    opentelemetry-exporter-otlp

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

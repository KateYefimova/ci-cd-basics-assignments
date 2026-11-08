FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
 
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 \
    COUNTER_FILE=/app/data/visits.txt
 
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
 
COPY --from=builder /install /usr/local
COPY app.py .
 
RUN mkdir -p /app/data && chown -R appuser:appuser /app
USER appuser
 
EXPOSE 8080
CMD ["python", "app.py"]
 
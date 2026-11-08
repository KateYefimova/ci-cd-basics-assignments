FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local

COPY . .

RUN mkdir -p /app/data && chown -R appuser:appuser /app

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8080

CMD ["python", "app.py"]
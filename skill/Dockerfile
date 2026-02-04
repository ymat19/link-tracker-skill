FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY tracker.py .

ENV PORT=59934
ENV LOG_PATH=/data/clicks.jsonl
ENV LOG_UA=false
ENV LOG_IP=false
ENV ALLOWED_DOMAINS=

EXPOSE 59934

CMD ["python", "tracker.py"]

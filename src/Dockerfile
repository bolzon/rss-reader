FROM python:3.9-slim-bullseye

WORKDIR /app

COPY rss/ ./rss/
COPY .env logging.ini requirements.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["uvicorn"]
CMD ["rss.reader.main:app", "--no-server-header"]

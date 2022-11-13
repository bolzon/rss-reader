FROM python:3.9-slim-bullseye

WORKDIR /app

COPY .env logging.ini requirements.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY rss/ ./rss/

ENTRYPOINT ["uvicorn"]
CMD ["rss.reader.main:main", "--no-server-header"]

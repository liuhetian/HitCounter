FROM python:3.13-slim
WORKDIR /app
RUN pip install --no-cache-dir --progress-bar off fastapi uvicorn sqlmodel
RUN mkdir -p /volume/dbs
COPY main.py /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

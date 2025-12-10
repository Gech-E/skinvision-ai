FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/backend

ENV PYTHONPATH=/app
ENV MODEL_PATH=/app/model/artifacts/model.h5
ENV LABEL_MAP_PATH=/app/model/label_map.json
ENV UPLOAD_DIR=/app/uploads

RUN mkdir -p /app/uploads

WORKDIR /app/backend

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]

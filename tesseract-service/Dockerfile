FROM python:3.11

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y tesseract-ocr

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install flask

CMD ["python", "main.py"]

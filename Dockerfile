FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 10000

CMD ["python", "app.py"]
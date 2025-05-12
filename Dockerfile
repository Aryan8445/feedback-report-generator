FROM python:3.13
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 
WORKDIR /app

COPY requirements.txt ./
# Install system dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000


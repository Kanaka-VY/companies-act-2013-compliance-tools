FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Bind 0.0.0.0 so Docker port publish works; use shell form so the factory target parses reliably.
CMD ["sh", "-c", "gunicorn -w 2 -b 0.0.0.0:8000 'app:create_app()'"]

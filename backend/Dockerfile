FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bake model into image to avoid 502 timeouts during first startup
COPY download_model.py .
RUN python3 download_model.py

COPY . .

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "debug", "--timeout-keep-alive", "60"]

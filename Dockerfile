FROM python:3.12-slim

# 1) Sistema base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 2) Dependencias
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copia del proyecto
COPY . /app

# 4) Exponer puerto
EXPOSE 8000

# 5) Comando default (dev con reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

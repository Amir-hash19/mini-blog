FROM python:3.12-slim

LABEL maintainer="amir-hash19"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /usr/src/app


COPY requirements.txt .


RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


    
COPY . .


RUN POSTGRES_DB=build_db \
    POSTGRES_USER=build_user \
    POSTGRES_PASSWORD=build_password \
    POSTGRES_HOST=localhost \
    POSTGRES_PORT=5432 \
    MONGO_INITDB_ROOT_USERNAME=build_user \
    MONGO_INITDB_ROOT_PASSWORD=build_password \
    MONGO_HOST=localhost \
    MONGO_PORT=27017 \
    python manage.py collectstatic --noinput

EXPOSE 8000


CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]

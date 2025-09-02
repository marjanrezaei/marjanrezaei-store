FROM python:3.10-slim-bookworm

LABEL maintainer="rezaei.marjann@gmail.com"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python core/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]

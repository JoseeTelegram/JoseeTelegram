FROM python:3.11.2-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR JoseeTelegram

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY josee_bot ./josee_bot

CMD ["python", "-m", "josee_bot"]
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY app ./app
COPY agents ./agents
COPY contracts ./contracts
COPY core ./core
COPY mcp ./mcp
COPY ops ./ops
COPY rag ./rag

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

COPY deploy/start.sh /app/deploy/start.sh

CMD ["/app/deploy/start.sh"]

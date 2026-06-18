FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=7860 \
    GRADIO_ANALYTICS_ENABLED=False

WORKDIR /app

COPY pyproject.toml README.md ./
COPY agents ./agents
COPY app ./app
COPY contracts ./contracts
COPY core ./core
COPY data ./data
COPY ops ./ops
COPY rag ./rag

RUN pip install --upgrade pip && pip install .

EXPOSE 7860

CMD ["python", "-m", "app.ui"]

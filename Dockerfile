FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PAI_WORKSPACE=/workspace \
    PAI_DB_PATH=/data/memory.sqlite3

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app \
    && mkdir -p /data /workspace \
    && chown -R app:app /data /workspace /app

COPY --chown=app:app pyproject.toml README.md ./
COPY --chown=app:app personal_ai_os ./personal_ai_os
COPY --chown=app:app main.py ./main.py

RUN pip install --upgrade pip \
    && pip install .

USER app

VOLUME ["/data", "/workspace"]
ENTRYPOINT ["personal-ai-os"]
CMD ["chat"]

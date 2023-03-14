# Stage 0 - Create from Python3.9.5 image
# FROM python:3.9-slim-buster as stage0
FROM python:3.9-slim-buster

# Stage 1 - Copy and execute module
# FROM stage0 as stage1
COPY requirements.txt /app/requirements.txt
RUN /usr/local/bin/python -m venv /app/env \
        && /app/env/bin/pip install -r /app/requirements.txt
COPY ./disable_renew.py /app/disable_renew.py

LABEL version="1.0" \
        description="Containerized disable_renew module."
ENTRYPOINT ["/app/env/bin/python3", "/app/disable_renew.py"]
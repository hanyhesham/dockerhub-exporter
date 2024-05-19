## WEB Builder Stage
FROM python:3.12.3-slim-bullseye AS builder

## Install Packages
RUN apt-get update \
    && apt-get clean \
    && apt-get autoclean \
    && apt-get autoremove --purge  -y \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

## Install python packages
COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --requirement /tmp/requirements.txt

## Final Stage
FROM python:3.12.3-slim-bullseye

## add non root user
RUN adduser debian

## Copy from builder and set ENV for venv
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

## Copy app files into container
WORKDIR /workspace/web
COPY ./src .

## Switch to non-priviliged user and run app
USER debian

## Expose port 2113
EXPOSE 2113

# ## Entrypoint for the container
ENTRYPOINT ["python3", "main.py"]
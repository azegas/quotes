# inspiration taken from here - https://github.com/devcontainers/images/blob/main/src/python/.devcontainer/Dockerfile

FROM mcr.microsoft.com/devcontainers/python:1-3.12

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements
COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip \
    && pip3 install -r requirements.txt \
    && rm -rf requirements.txt

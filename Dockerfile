FROM python:3.9-alpine3.12

# Copy requirments and moving to workdir
COPY requirements.txt /sql_automation/requirements.txt
WORKDIR /sql_automation

# Update apk repo
RUN echo "https://dl-4.alpinelinux.org/alpine/v3.12/main" >> /etc/apk/repositories
RUN echo "https://dl-4.alpinelinux.org/alpine/v3.12/community" >> /etc/apk/repositories

# Install automation dependencies
RUN apk update
RUN apk add chromium chromium-chromedriver
RUN apk add libressl-dev musl-dev libffi-dev gcc

# Upgrade pip and prepare env
RUN pip install --upgrade pip
RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r requirements.txt

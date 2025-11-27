ARG PYTHON_VERSION=3.11-slim-bullseye
FROM python:${PYTHON_VERSION}

# Upgrade pip
RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# copy the project code into the container's working directory
COPY . .

EXPOSE 8000
# Install the Python project requirements
RUN pip install -r requirements.txt

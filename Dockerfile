# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean

# Copy project
COPY . /code/

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . /code/

# Expose port
EXPOSE 8000

# Run the command to start uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

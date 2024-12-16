# Use Ubuntu as the base image
FROM ubuntu:latest

# Set the timezone
ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Update the package list and install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    python3 \
    python3-pip \
    python3-venv

# Create and set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Create a virtual environment and install the requirements
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install --upgrade pip
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Set the environment to use the virtual environment by default
ENV PATH="/app/venv/bin:$PATH"

# Run the script
CMD ["python3", "main.py"]

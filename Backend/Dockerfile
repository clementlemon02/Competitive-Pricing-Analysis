# Use the official Python image
FROM python:3.8-slim

# Install pkg-config and other necessary dependencies
RUN apt-get update \
    && apt-get install -y \
        pkg-config \
        libmariadb-dev-compat \
        net-tools \
        telnet \
        mariadb-client \
        gcc \
        python3-dev \
        default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Specify the command to run your application
CMD ["python", "app.py", "--host=0.0.0.0"]

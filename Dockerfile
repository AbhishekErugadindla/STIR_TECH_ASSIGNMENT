FROM python:3.12

# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Copy and execute Chrome installation script
COPY build.sh /build.sh
RUN chmod +x /build.sh && /build.sh

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Set environment variable for Chrome
ENV GOOGLE_CHROME_BIN=/usr/bin/google-chrome

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
FROM cypress/browsers:latest

# Install Python
RUN apt-get install python3 -y

RUN echo $(python3 -m site --user-base)

# Copy requirements file
COPY requirements.txt .

# Set PATH
ENV PATH /home/root/.local/bin:${PATH}

# Install pip and requirements
RUN apt-get update && apt-get install -y python3-pip && pip install -r requirements.txt

# Copy application files
COPY . .

# Run with uvicorn
CMD uvicorn main:app --host 0.0.0.0 --port $PORT

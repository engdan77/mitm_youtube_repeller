# Use a base Python image
FROM python:3.11.1

WORKDIR /app

COPY ./src/script.py .
COPY ./src/start.sh .

RUN pip install mitmproxy loguru

EXPOSE 8080

# Define the command to start the app
CMD ["bash", "/app/start.sh"]
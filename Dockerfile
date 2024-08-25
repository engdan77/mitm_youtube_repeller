# Use a base Python image
FROM python:3.11.1

WORKDIR /app

COPY ./src/script.py .

RUN pip install mitmproxy loguru

EXPOSE 8080

# Define the command to start the app
CMD ["mitmdump", "--mode", "regular", "--set", "keep_host_header", "--set validate_inbound_headers=false", "-s", "/app/script.py"]
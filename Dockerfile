FROM ubuntu:latest
FROM python:3.9-slim
# Copy the model file to the working directory

# Set the working directory in the container
WORKDIR /app
COPY food101.h5 .
COPY nutri.csv .
# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080


# Copy the application code to the working directory
COPY main.py .

# Expose the port on which the Flask app will run

# Set the entrypoint command to run the Flask app
CMD ["python", "main.py"]

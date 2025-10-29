# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /code

# Copy the requirements file and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code
COPY ./app /code/app
# Expose the port the app runs on
EXPOSE 80

# Command to run the application
# Use --host 0.0.0.0 to make it accessible outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
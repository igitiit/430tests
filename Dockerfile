# Use Python 3.10 as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app/

# Specify the command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "blog_project.wsgi:application"]

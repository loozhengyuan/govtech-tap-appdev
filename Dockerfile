# Use python3 image
FROM python:3-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy files
COPY govgrant/ govgrant/
COPY manage.py manage.py
COPY entrypoint.sh entrypoint.sh

# Create unprivileged system user
# The -l flag is used as a workaround due to an unresolved bug:
# https://github.com/golang/go/issues/13548
RUN groupadd -r docker && useradd -l -r -s /bin/false -g docker docker
RUN chown -R docker:docker /app
USER docker

# Set entrypoint
RUN chmod a+x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

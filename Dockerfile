FROM python:3.10-slim

WORKDIR /app

# Copy the application files
COPY . /app

# Install system dependencies required for numpy and scikit-learn
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    gfortran \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install scikit-learn==1.3.2
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "src.app:app", "--bind", "0.0.0.0:5000"]
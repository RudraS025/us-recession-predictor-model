FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Upgrade pip and install scikit-learn 1.5.2 first
RUN pip install --upgrade pip
RUN pip install scikit-learn==1.5.2

# Install the remaining dependencies
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "src.app:app", "--bind", "0.0.0.0:5000"]
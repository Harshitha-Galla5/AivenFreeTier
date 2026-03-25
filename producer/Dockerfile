FROM python:3.12-slim

# create non-root user
RUN useradd -m appuser

# set working directory
WORKDIR /app

# copy only requirements first 
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy app files
COPY . .

# change ownership to non-root user
RUN chown -R appuser:appuser /app

# switch to non-root user
USER appuser

# run app
CMD ["python", "producer.py"]

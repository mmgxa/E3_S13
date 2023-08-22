FROM python:3.10-slim

WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir --upgrade -r requirements.txt

# Copy the app
COPY server.py /app/server.py

# Expose the app's port
EXPOSE 9080

# Run the FastAPI server
ENTRYPOINT ["python"] 
CMD ["server.py"]

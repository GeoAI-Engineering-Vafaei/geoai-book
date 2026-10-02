# 1) start from an official, slim Python base image
FROM python:3.12-slim
# 2) set the working directory inside the container
WORKDIR /app
# 3) install dependencies first (better build caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# 4) copy the rest of the application code and the model
COPY . .
# 5) expose the port and run the server
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

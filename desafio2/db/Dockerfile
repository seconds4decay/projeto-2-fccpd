FROM python:3.12-slim

WORKDIR /app
COPY app.py .
COPY requiremets.txt .

RUN pip install -r requiremets.txt

EXPOSE 8080
CMD ["python", "app.py"]

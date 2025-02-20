FROM python3.10

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --update -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "fastapi:app",  "--host", "0.0.0.0", "--port", "8080"]

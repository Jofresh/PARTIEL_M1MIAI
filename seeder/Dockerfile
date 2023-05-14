FROM python:3.10-alpine

WORKDIR /app

RUN pip install pymongo

COPY . .

CMD ["python", "seeder.py"]

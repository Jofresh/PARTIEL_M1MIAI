FROM python:3.10-alpine

WORKDIR /app

RUN pip install pymongo pydantic fastapi uvicorn

COPY . .

EXPOSE 4850

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "4850"]

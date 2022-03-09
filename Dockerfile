FROM python:3.8.2-alpine

WORKDIR ../Lab_1

COPY . .

CMD ["python","Lab1.py"]

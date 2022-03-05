FROM python:3.8

WORKDIR ../Lab_1

COPY . .

CMD ["python","Lab1.py"]

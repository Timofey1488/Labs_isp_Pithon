FROM python:3.8-alpine

WORKDIR ../Labs_isp_Pithon/Lab_1/lab1.py

COPY . .

CMD ["python","lab1.py"]

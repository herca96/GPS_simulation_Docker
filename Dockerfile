FROM python:3.11.0

WORKDIR /app

RUN pip install mysql-connector==2.2.9

CMD [ "python3", "gps_simulation.py"]

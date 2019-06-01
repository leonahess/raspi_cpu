FROM python:alpine

ADD app ./app
ADD requirements.txt .
ADD config.py .
ADD smarthome_raspi.py .

WORKDIR .

RUN pip3 install -r requirements.txt

CMD ["python3", "smarthome_raspi.py"]

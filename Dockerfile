FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./pyscript/data-write.py ./

CMD ["python", "-u", "data-write.py"]

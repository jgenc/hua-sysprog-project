FROM python:3.12

WORKDIR /

COPY ./consumers /consumers

RUN pip install -r ./consumers/requirements.txt

ENTRYPOINT [ "python", "consumers/main.py" ]
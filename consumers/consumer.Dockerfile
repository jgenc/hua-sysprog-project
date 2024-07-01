FROM python:3.12

ENV BOOTSTRAP_SERVER=localhost:9094
ENV TOPICS=""

WORKDIR /

COPY ./consumers /consumers

RUN pip install -r ./consumers/requirements.txt

ENTRYPOINT [ "python", "consumers/main.py" ]
FROM python:3.12

ENV BOOTSTRAP_SERVER=localhost:9094

WORKDIR /

COPY ./producers /producers

RUN pip install -r ./producers/requirements.txt

EXPOSE 8099/tcp

ENTRYPOINT [ "python", "-m", "producers.main" ]
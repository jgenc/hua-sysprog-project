FROM python:3.12

WORKDIR /

COPY ./api /api/

RUN pip install -r ./api/requirements.txt

EXPOSE 8098/tcp

ENTRYPOINT [ "python", "-m", "api.main" ]
FROM python:3.12

ENV PORT=8098

WORKDIR /

COPY ./api /api

RUN pip install -r ./api/requirements.txt

EXPOSE ${PORT}/tcp

ENTRYPOINT [ "python", "-m", "api.main" ]
# hua-sysprog-project

## Table of Contents

!TODO

## Local installation

### `conda` environemnt

To initialize the appropriate Python environemnt a `conda` installation is recommended.
Run the following line to install and use the environemnt.

```bash
conda env create -f environment.yml
conda activate sys_prog
```

### Run the API

```bash
python -m api.main
```

### Populate the dummy data file

To upload some dummy data in the dummy database, please run the following lines while the API is running:

```bash
python -m api.data.create_dummy
python -m api.data.upload_dummy
```

Now the sqlite database contains some dummy data examples.

## Docker

### `docker-compose` installation and usage

Fill in

### Containers

#### `consumer`

##### Environment variables

- `BOOTSTRAP_SERVER`: The kafka server that the producer should be listening to. Defaults to `localhost:9094`. **Required**
- `TOPICS`: Either a single string or a list of comma separated strings of topics. No default value. **Required**

##### Usage

Build the container without a tag:

```bash
docker build . -f consumers/consumer.Dockerfile
```

or additionally provide a tag

```bash
docker build -t hua-sysprog-project-consumers . -f consumers/consumer.Dockerfile
```

Run the container using the following

```bash
docker run \
    -e TOPICS="test_topic" \
    -e BOOTSTRAP_SERVER="0.0.0.0:2994" \
    hua-sysprog-project-consumer:latest
```

> Keep in mind that if you do not want to use the docker-compose solution you will have to
> manually start a kafka server and point the consumer to the correct IP and port
> using the `BOOTSTRAP_SERVER` environemnt variable

#### `producer`

##### Environment variables

- `BOOTSTRAP_SERVER`: The kafka server that the producer should be listening to. Defaults to `localhost:9094`. **Required**

##### Usage

Build the container without a tag:

```bash
docker build . -f consumers/consumer.Dockerfile
```

or additionally provide a tag

```bash
docker build -t hua-sysprog-project-consumers . -f consumers/consumer.Dockerfile
```

Run the container using the following

```bash
docker run \
    -e BOOTSTRAP_SERVER="0.0.0.0:2994" \
    hua-sysprog-project-producer:latest
```

> Keep in mind that if you do not want to use the docker-compose solution you will have to
> manually start a kafka server and point the producer to the correct IP and port
> using the `BOOTSTRAP_SERVER` environemnt variable

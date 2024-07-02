# hua-sysprog-project <!-- omit in toc -->

## Introduction <!-- omit in toc -->

![](./assets/hua.png)

This repository houses the code for the project of the "Systems Programming" Lecture, conducted at Harokopio's University of Athens (HUA) Department of Informatics and Telematics (DIT).

## Table of Contents <!-- omit in toc -->

- [Architecture](#architecture)
  - [Summary](#summary)
  - [Notes](#notes)
- [Usage](#usage)
- [Performance](#performance)
  - [Dummy uploads](#dummy-uploads)
- [Installation](#installation)
  - [Local installation](#local-installation)
    - [`conda` environemnt](#conda-environemnt)
    - [Run the API](#run-the-api)
    - [Populate the dummy data file](#populate-the-dummy-data-file)
  - [Docker](#docker)
    - [`docker-compose` installation and usage](#docker-compose-installation-and-usage)
    - [Containers](#containers)
      - [`api`](#api)
        - [Environment variables](#environment-variables)
        - [Usage](#usage-1)
      - [`consumer`](#consumer)
        - [Environment variables](#environment-variables-1)
        - [Usage](#usage-2)
      - [`producer`](#producer)
        - [Environment variables](#environment-variables-2)
        - [Usage](#usage-3)
- [Development](#development)

## Architecture

![](./assets/SysProg%20Arch.svg)

### Summary

A list of clients (in this case, just one) send the user, coupon and event data to the system using a kafka producer (or multiple, depending on the configuration). Each class of data is produced in its own topic. The default configuration of the system will create one kafka consumer for each topic. The consumers send the data to the corresponding endpoint of the API. That data is stored in a datastore, in this case it's an sqlite database. The recommendation generator algorithm produces recommendations based on the frequency of the betting sport of each user. The generation process is executed every time an event is uploaded to the system *or*, additionally, it can be executed manually, using the corresponding endpoint. The consumers/end-users of the system can access their recommendations by providing their Id to the /recommendations/{user_id} endpoint.

### Notes

- There is **one** database which is indicated by the gray color. Different "database icons" have been used to indicate different tables of the database.
- Producers and consumers are made using the [AIOKafka](https://github.com/aio-libs/aiokafka) Python library.
- The SQL database can be easily changed in [/api/dependencies/database.py](./api/dependencies/database.py) by modifying the URL used in `create_engine`. [sqlmodel](https://sqlmodel.tiangolo.com/) is used to handle model files and the ORM of the whole project, which works great with [FastAPI](https://fastapi.tiangolo.com/) -- the framework used to develop the system's API.

## Usage

API usage, endpoints, etc.

## Performance

### Dummy uploads

CPU Used: Apple M3 Pro, 12-core

Configuration: docker-compose

Uploading concurrently a list of dummy data for each entity of users, events and coupons using an external httpx server (file is found in [create_dummy.py](./api/data/create_dummy.py)) takes the following time:

| Entity      | Amount      | Time (seconds) |
| ----------- | ----------- | ---   |
| Users | 100| 2.6263 |
| Events| 100| 2.4140 |
| Coupons|  100 | 2.4488|

*Note:* Docker in MacOS is notoriously known for its slow performance. No optimizations were done to improve the time of the run

## Installation

### Local installation

#### `conda` environemnt

To initialize the appropriate Python environemnt a `conda` installation is recommended.
Run the following line to install and use the environemnt.

```bash
conda env create -f environment.yml
conda activate sys_prog
```

#### Run the API

```bash
python -m api.main
```

#### Populate the dummy data file

To upload some dummy data in the dummy database, please run the following lines while the API is running:

```bash
python -m api.data.create_dummy
python -m api.data.upload_dummy
```

Now the sqlite database contains some dummy data examples.

### Docker

#### `docker-compose` installation and usage

Using the provided [compose.yaml](./compose.yaml) file that incorporates all the containers listed below, in addition to the kafka container and configuration, you can easily install and run the whole system using the following command:

```bash
docker compose up
```

#### Containers

> [!IMPORTANT]
> Keep in mind that if you do not want to use the docker-compose solution you will have to
> manually start a kafka server and point the the producer and consumer containers
> to the correct IP and port using the `BOOTSTRAP_SERVER` environemnt variable available
> in both containers.

##### `api`

###### Environment variables

- `PORT`: Indicates the port that the container will expose. Should be a string. Defaults to `"8098"`. **Required**

###### Usage

Build the container without a tag:

```bash
docker build . -f api/api.Dockerfile
```

or additionally provide a tag

```bash
docker build -t hua-sysprog-project-api . -f api/api.Dockerfile
```

Run the container using the following

```bash
docker run \
    -e PORT="8098" \
    hua-sysprog-project-api:latest
```

##### `consumer`

###### Environment variables

- `BOOTSTRAP_SERVER`: The kafka server that the producer should be listening to. Defaults to `localhost:9094`. **Required**
- `TOPICS`: Either a single string or a list of comma separated strings of topics. No default value. **Required**

###### Usage

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

##### `producer`

###### Environment variables

- `BOOTSTRAP_SERVER`: The kafka server that the producer should be listening to. Defaults to `localhost:9094`. **Required**

###### Usage

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

## Development

Development of each module is done locally first.

Take note of the following caveats for local environemnt to work correctly:

1. To generate a local `sqlite` database when running the API you'll need to do the run the api using this command: `ENV=dev python -m api.main`

> [!WARNING]
> This environment variable needs to be added in every local execution of the modules and submodules. For example, if you want to run the main function of [api/recommendations/frequency.py](./api/recommendations/frequency.py) you will need to include this, as the program will not know the correct path to the database.

2. To upload the dummy data created in [create_dummy.py](./api/data/create_dummy.py) and uploaded using [upload_dummy.py](./api/data/upload_dummy.py) please specify the port of the API using the following environemnt variable: `PORT=8098 python -m api.data.upload_dummy`
   1. The default behaviour of upload_dummy is to point to the docker-compose instance of the API. With this environemnt variable change you can point to whatever port the API works in

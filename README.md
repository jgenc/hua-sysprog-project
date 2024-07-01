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

- `TOPICS`: Either a single string or a list of comma separated strings of topics

##### Usage

Build the container without a tag:

```bash
docker build . -f consumers/consumer.Dockerfile
```

or additionally provide a tag

```bash
docker build -t hua-sysprog-consumers . -f consumers/consumer.Dockerfile
```

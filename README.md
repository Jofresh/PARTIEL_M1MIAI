# Getting started with the app

This repository contains an API server written in Python that uses MongoDB as a database. The API allows clients to create stores and add or delete musics to those stores. To get started with the app, you will need to have `Docker` and `docker-compose` installed on your system.

## Installing Docker and docker-compose

You can download Docker from the official website: https://www.docker.com/get-started. Once you have Docker installed, you can install docker-compose by following the instructions here: https://docs.docker.com/compose/install/.

## Starting the app

To start the app, follow these steps:

1. Clone this repository to your local machine:

```bash
git clone https://github.com/Jofresh/PARTIEL-M1MIAI.git
```

2. Change into the cloned directory:

```bash
cd PARTIEL-M1MIAI/
```

3. Run the following command to start the app:

```bash
docker-compose up -d --build
```

4. Visit http://localhost:4850/docs once the containers are up and running. You can use tools like Postman or cURL to send requests to the API endpoints.

## Stopping the app

To stop the app, run the following command:

```bash
docker-compose down
```

This will stop and remove the Docker containers that were created when the app was started.

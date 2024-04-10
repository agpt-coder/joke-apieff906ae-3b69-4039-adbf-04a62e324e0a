---
date: 2024-04-10T19:19:13.347961
author: AutoGPT <info@agpt.co>
---

# joke api

To create a Joke API that outputs a single random joke at the endpoint `/joke`, using the specified tech stack (Python, FastAPI, PostgreSQL, Prisma), follow these comprehensive steps:

1. **Setup Environment**: Ensure Python is installed. Create a virtual environment and activate it.

2. **Install Dependencies**: Install FastAPI and Uvicorn as ASGI server using pip. Since the project involves PostgreSQL and Prisma, also install asyncpg and prisma-client with pip.

3. **Initialize Prisma**: Initialize Prisma in your project directory, define your Joke model within `schema.prisma` file, and update the database schema using Prisma migrations.

4. **Seed Database**: Populate your PostgreSQL database with a variety of jokes. Use Prisma's seed feature or manually insert jokes into your database.

5. **Develop FastAPI Application**: Create a Python file, for instance, `main.py`. Import FastAPI, and from prisma-client import Prisma. Instantiate FastAPI and Prisma objects.

6. **Database Connection**: Ensure your Prisma client connects to the database asynchronously upon app startup and disconnects when the app is shutting down, by utilizing FastAPI events.

7. **Create Endpoint**: Define an endpoint `/joke` with a GET method. Inside the function, query the database asynchronously to fetch a random joke. There are several ways to retrieve a random row from PostgreSQL. One approach is to order by RANDOM() function and limit the result to 1.

8. **Return Joke**: Once the joke is fetched, return it in JSON format.

9. **Run the Application**: Use Uvicorn to run your FastAPI application. Ensure to specify the `main:app` with `--reload` for development. Open your browser or use a tool like Postman to test the `/joke` endpoint.

Here is an example code snippet for the endpoint:

```python
from fastapi import FastAPI
from prisma import Prisma, models

app = FastAPI()
prisma = Prisma()

@app.on_event('startup')
async def startup_event():
    await prisma.connect()

@app.on_event('shutdown')
async def shutdown_event():
    await prisma.disconnect()

@app.get('/joke')
async def read_joke():
    joke = await prisma.joke.find_many(order={'random()': True}, take=1)
    return {'joke': joke[0].text if joke else 'No jokes available.'}
```

Ensure you have the Joke model defined within your Prisma schema and the database seeded with jokes for this to work. Now, visiting `/joke` will return a random joke from your database.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'joke api'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow

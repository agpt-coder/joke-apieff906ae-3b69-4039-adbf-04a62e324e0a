import logging
from contextlib import asynccontextmanager

import project.read_joke_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="joke api",
    lifespan=lifespan,
    description="To create a Joke API that outputs a single random joke at the endpoint `/joke`, using the specified tech stack (Python, FastAPI, PostgreSQL, Prisma), follow these comprehensive steps:\n\n1. **Setup Environment**: Ensure Python is installed. Create a virtual environment and activate it.\n\n2. **Install Dependencies**: Install FastAPI and Uvicorn as ASGI server using pip. Since the project involves PostgreSQL and Prisma, also install asyncpg and prisma-client with pip.\n\n3. **Initialize Prisma**: Initialize Prisma in your project directory, define your Joke model within `schema.prisma` file, and update the database schema using Prisma migrations.\n\n4. **Seed Database**: Populate your PostgreSQL database with a variety of jokes. Use Prisma's seed feature or manually insert jokes into your database.\n\n5. **Develop FastAPI Application**: Create a Python file, for instance, `main.py`. Import FastAPI, and from prisma-client import Prisma. Instantiate FastAPI and Prisma objects.\n\n6. **Database Connection**: Ensure your Prisma client connects to the database asynchronously upon app startup and disconnects when the app is shutting down, by utilizing FastAPI events.\n\n7. **Create Endpoint**: Define an endpoint `/joke` with a GET method. Inside the function, query the database asynchronously to fetch a random joke. There are several ways to retrieve a random row from PostgreSQL. One approach is to order by RANDOM() function and limit the result to 1.\n\n8. **Return Joke**: Once the joke is fetched, return it in JSON format.\n\n9. **Run the Application**: Use Uvicorn to run your FastAPI application. Ensure to specify the `main:app` with `--reload` for development. Open your browser or use a tool like Postman to test the `/joke` endpoint.\n\nHere is an example code snippet for the endpoint:\n\n```python\nfrom fastapi import FastAPI\nfrom prisma import Prisma, models\n\napp = FastAPI()\nprisma = Prisma()\n\n@app.on_event('startup')\nasync def startup_event():\n    await prisma.connect()\n\n@app.on_event('shutdown')\nasync def shutdown_event():\n    await prisma.disconnect()\n\n@app.get('/joke')\nasync def read_joke():\n    joke = await prisma.joke.find_many(order={'random()': True}, take=1)\n    return {'joke': joke[0].text if joke else 'No jokes available.'}\n```\n\nEnsure you have the Joke model defined within your Prisma schema and the database seeded with jokes for this to work. Now, visiting `/joke` will return a random joke from your database.",
)


@app.get("/joke", response_model=project.read_joke_service.FetchJokeResponse)
async def api_get_read_joke() -> project.read_joke_service.FetchJokeResponse | Response:
    """
    Fetches a single random joke from the database and returns it in a JSON format.
    """
    try:
        res = await project.read_joke_service.read_joke()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )

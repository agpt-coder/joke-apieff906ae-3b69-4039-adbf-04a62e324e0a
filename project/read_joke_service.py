from typing import Optional

from prisma import Prisma
from pydantic import BaseModel


class FetchJokeResponse(BaseModel):
    """
    This model structures the response of a fetched random joke, encapsulating it within a JSON format for ease of use in client applications.
    """

    joke: str
    id: str
    createdAt: str
    submittedBy: Optional[str] = None


async def read_joke() -> FetchJokeResponse:
    """
    Fetches a single random joke from the database and returns it in a JSON format.

    Args:


    Returns:
    FetchJokeResponse: This model structures the response of a fetched random joke, encapsulating it within a JSON format for ease of use in client applications.

    Example:
    # Assuming there's a joke in the database
    read_joke()
    > FetchJokeResponse(joke="Why did the function stop calling? Because it reached its call limit!", id="1234-5678-9012",
                        createdAt="2023-01-01T00:00:00", submittedBy="John Doe")
    """
    prisma = Prisma()
    async with prisma:
        jokes = await prisma.joke.find_many(order={"random()": True}, take=1)
        if jokes:
            joke = jokes[0]
            return FetchJokeResponse(
                joke=joke.text,
                id=joke.id,
                createdAt=joke.createdAt.isoformat(),
                submittedBy=joke.submittedBy,
            )
        else:
            raise Exception("No jokes available in the database.")

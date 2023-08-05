from typing import *
import datetime
import uuid
import royalnet.utils as ru
import royalnet.constellation.api as rca
from ..tables import Poll


class ApiPollStar(rca.ApiStar):
    path = "/api/poll/v2"

    parameters = {
        "get": {
            "uuid": "The UUID of the poll to get.",
        },
        "post": {
            "question": "The question to ask in the poll.",
            "description": "A longer Markdown-formatted description.",
            "expires": "A ISO timestamp of the expiration date for the poll.",
        }
    }

    auth = {
        "get": False,
        "post": True
    }

    tags = ["poll"]

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get a specific poll."""
        PollT = self.alchemy.get(Poll)

        try:
            pid = uuid.UUID(data["uuid"])
        except (ValueError, AttributeError, TypeError):
            raise rca.InvalidParameterError("'uuid' is not a valid UUID.")

        poll: Poll = await ru.asyncify(data.session.query(PollT).get, pid)
        if poll is None:
            raise rca.NotFoundError("No such page.")

        return poll.json()

    @rca.magic
    async def post(self, data: rca.ApiData) -> ru.JSON:
        """Create a new poll."""
        PollT = self.alchemy.get(Poll)

        poll = PollT(
            id=uuid.uuid4(),
            creator=await data.user(),
            created=datetime.datetime.now(),
            expires=datetime.datetime.fromisoformat(data["expires"]) if "expires" in data else None,
            question=data["question"],
            description=data.get("description"),
        )

        data.session.add(poll)
        await data.session_commit()

        return poll.json()

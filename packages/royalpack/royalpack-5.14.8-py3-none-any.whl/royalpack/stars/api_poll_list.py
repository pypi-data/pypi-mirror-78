from typing import *
import royalnet.constellation.api as rca
import royalnet.utils as ru
from ..tables import Poll


class ApiPollsListStar(rca.ApiStar):
    path = "/api/poll/list/v2"

    tags = ["poll"]

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get a list of all polls."""
        PollT = self.alchemy.get(Poll)

        polls: List[Poll] = await ru.asyncify(data.session.query(PollT).all)

        return list(map(lambda p: {
            "id": p.id,
            "question": p.question,
            "creator": p.creator.json(),
            "expires": p.expires.isoformat(),
            "created": p.created.isoformat(),
        }, polls))

import royalnet.constellation.api as rca
import royalnet.utils as ru
from ..tables import *


class ApiDiarioGetStar(rca.ApiStar):
    path = "/api/diario/v2"

    parameters = {
        "get": {
            "id": "The id of the diario entry to get."
        }
    }

    tags = ["diario"]

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get a specific diario entry."""
        diario_id = data.int("id")
        entry: Diario = await ru.asyncify(data.session.query(self.alchemy.get(Diario)).get, diario_id)
        if entry is None:
            raise rca.NotFoundError("No such diario entry.")
        return entry.json()

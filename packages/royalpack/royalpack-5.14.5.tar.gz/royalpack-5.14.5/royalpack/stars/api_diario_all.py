from typing import *
import royalnet.constellation.api as rca
import royalnet.utils as ru
from ..tables import *


class ApiDiarioAllStar(rca.ApiStar):
    path = "/api/diario/all/v2"

    tags = ["diario"]

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get all diario entries."""
        entries: List[Diario] = await ru.asyncify(
            data.session
                .query(self.alchemy.get(Diario))
                .order_by(self.alchemy.get(Diario).diario_id)
                .all
        )
        response = [entry.json() for entry in entries]
        return response

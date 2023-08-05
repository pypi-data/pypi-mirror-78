from typing import *
import royalnet.constellation.api as rca
import royalnet.utils as ru
from ..tables import *


class ApiDiarioRangeStar(rca.ApiStar):
    path = "/api/diario/range/v3"

    tags = ["diario"]

    parameters = {
        "get": {
            "start": "The starting diario_id (included).",
            "end": "The final diario_id (excluded).",
        }
    }

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get the diario entries in the specified range."""
        DiarioT = self.alchemy.get(Diario)

        entries: List[Diario] = await ru.asyncify(
            data.session
                .query(DiarioT)
                .filter(
                    DiarioT.diario_id >= data.int("start", optional=False),
                    DiarioT.diario_id < data.int("end", optional=False)
                )
                .order_by(DiarioT.diario_id)
                .all
        )
        response = [entry.json() for entry in entries]
        return response

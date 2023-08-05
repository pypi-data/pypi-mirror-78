from typing import *
import royalnet.constellation.api as rca
import royalnet.utils as ru
from ..tables import *
from sqlalchemy import func


class ApiDiarioLatestStar(rca.ApiStar):
    path = "/api/diario/latest/v3"

    parameters = {
        "get": {
            "amount": "The number of diario entries to get."
        }
    }

    tags = ["diario"]

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get the latest diario entries."""
        DiarioT = self.alchemy.get(Diario)

        entries: List[Diario] = await ru.asyncify(
            data.session
                .query(DiarioT)
                .order_by(func.random())
                .limit(data.int("amount", optional=False))
                .all
        )
        return list(map(lambda e: e.json(), entries))

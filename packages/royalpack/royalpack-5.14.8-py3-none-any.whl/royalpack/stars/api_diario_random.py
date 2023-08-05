from typing import *
import royalnet.constellation.api as rca
import royalnet.utils as ru
from ..tables import *
from sqlalchemy import func


class ApiDiarioRandomStar(rca.ApiStar):
    path = "/api/diario/random/v1"

    parameters = {
        "get": {
            "amount": "The number of diario entries to get."
        }
    }

    tags = ["diario"]

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get random diario entries."""
        DiarioT = self.alchemy.get(Diario)
        try:
            amount = int(data["amount"])
        except ValueError:
            raise rca.InvalidParameterError("'amount' is not a valid int.")
        entries: List[Diario] = await ru.asyncify(
            data.session
                .query(DiarioT)
                .order_by(func.random())
                .limit(amount)
                .all
        )
        if len(entries) < amount:
            raise rca.NotFoundError("Not enough diario entries.")
        return list(map(lambda e: e.json(), entries))

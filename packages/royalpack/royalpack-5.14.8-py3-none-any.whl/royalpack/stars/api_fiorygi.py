from typing import *
import royalnet.utils as ru
import royalnet.backpack.tables as rbt
import royalnet.constellation.api as rca
from ..tables import Fiorygi


class ApiFiorygiStar(rca.ApiStar):
    path = "/api/fiorygi/v2"

    parameters = {
        "get": {
            "uid": "The user to get the fiorygi of."
        }
    }

    tags = ["fiorygi"]

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get fiorygi information about a specific user."""
        user = await rbt.User.find(self.alchemy, data.session, data.int("uid"))
        if user.fiorygi is None:
            return {
                "fiorygi": 0,
                "transactions": [],
                "warning": "No associated fiorygi table"
            }
        fiorygi: Fiorygi = user.fiorygi
        transactions: ru.JSON = sorted(fiorygi.transactions, key=lambda t: -t.id)
        return {
            "fiorygi": fiorygi.fiorygi,
            "transactions": list(map(lambda t: {
                "id": t.id,
                "change": t.change,
                "reason": t.reason,
                "timestamp": t.timestamp.isoformat() if t.timestamp else None
            }, transactions))
        }

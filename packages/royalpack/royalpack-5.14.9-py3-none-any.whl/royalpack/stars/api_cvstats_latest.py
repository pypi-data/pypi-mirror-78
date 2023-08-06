import royalnet.utils as ru
import royalnet.constellation.api as rca
from ..tables import Cvstats


class ApiCvstatsLatestStar(rca.ApiStar):
    path = "/api/cvstats/latest/v1"

    tags = ["cvstats"]

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get the latest 500 cvstats recorded."""
        CvstatsT = self.alchemy.get(Cvstats)

        cvstats = data.session.query(CvstatsT).order_by(CvstatsT.timestamp.desc()).limit(500).all()

        return list(map(lambda c: c.json(), cvstats))

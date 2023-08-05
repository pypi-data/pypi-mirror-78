import royalnet.utils as ru
import royalnet.backpack.tables as rbt
import royalnet.constellation.api as rca
from ..tables import Bio


class ApiBioSetStar(rca.ApiStar):
    path = "/api/bio/v2"

    parameters = {
        "get": {
            "uid": "The id of the user to get the bio of."
        },
        "put": {
            "contents": "The contents of the bio."
        }
    }

    auth = {
        "get": False,
        "put": True,
    }

    tags = ["bio"]

    @rca.magic
    async def get(self, data: rca.ApiData) -> ru.JSON:
        """Get the bio of a specific user."""
        user = await rbt.User.find(self.alchemy, data.session, data.int("uid"))
        return user.bio.json() if user.bio else None

    @rca.magic
    async def put(self, data: rca.ApiData) -> ru.JSON:
        """Set the bio of current user."""
        contents = data["contents"]
        BioT = self.alchemy.get(Bio)
        user = await data.user()
        bio = user.bio
        if bio is None:
            bio = BioT(user=user, contents=contents)
            data.session.add(bio)
        else:
            bio.contents = contents
        await data.session_commit()
        return bio.json()

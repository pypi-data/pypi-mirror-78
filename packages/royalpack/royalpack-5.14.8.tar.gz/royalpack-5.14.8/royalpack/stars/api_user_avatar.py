import re
import royalnet.utils as ru
import royalnet.constellation.api as rca


url_validation = re.compile(r'^(?:http|ftp)s://'
                            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                            r'localhost|'
                            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                            r'(?::\d+)?'
                            r'(?:/?|[/?]\S+)$', re.IGNORECASE)


class ApiUserAvatarStar(rca.ApiStar):
    path = "/api/user/avatar/v2"

    parameters = {
        "put": {
            "avatar_url": "The url that the user wants to set as avatar. MUST BE HTTPS/FTPS!"
        }
    }

    auth = {
        "put": True,
    }

    tags = ["user"]

    @rca.magic
    async def put(self, data: rca.ApiData) -> ru.JSON:
        """Set the avatar of current user."""
        avatar_url = data["avatar_url"]
        user = await data.user()
        if not re.match(url_validation, avatar_url):
            raise rca.InvalidParameterError("avatar_url is not a valid url.")
        user.avatar_url = avatar_url
        await data.session_commit()
        return user.json()

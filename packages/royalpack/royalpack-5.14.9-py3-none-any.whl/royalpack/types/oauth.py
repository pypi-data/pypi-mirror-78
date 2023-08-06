import aiohttp


async def oauth_auth(*, url, client_id, client_secret, redirect_uri, auth_code):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }) as response:
            j = await response.json()
            return j


async def oauth_refresh(*, url, client_id, client_secret, refresh_code):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_code,
            "grant_type": "refresh_token"
        }) as response:
            j = await response.json()
            return j

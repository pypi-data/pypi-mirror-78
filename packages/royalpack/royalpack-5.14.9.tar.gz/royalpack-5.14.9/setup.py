# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalpack',
 'royalpack.commands',
 'royalpack.commands.abstract',
 'royalpack.events',
 'royalpack.stars',
 'royalpack.tables',
 'royalpack.types',
 'royalpack.utils']

package_data = \
{'': ['*']}

install_requires = \
['bcrypt>=3.1.7,<4.0.0',
 'itsdangerous>=1.1.0,<2.0.0',
 'riotwatcher>=3.0.0,<4.0.0',
 'royalnet[telegram,discord,alchemy_easy,constellation,sentry,herald,coloredlogs]>=5.11.9,<5.12.0',
 'royalspells>=3.2,<4.0',
 'sqlalchemy>=1.3.18,<2.0.0',
 'steam']

setup_kwargs = {
    'name': 'royalpack',
    'version': '5.14.9',
    'description': 'A Royalnet command pack for the Royal Games community',
    'long_description': '# `royalpack`\n\n## Configuration\n\n```toml\n[Packs."royalpack"]\n\n# The main Telegram group\nTelegram.main_group_id = -1001153723135\n\n# The main Discord channel\nDiscord.main_channel_id = 566023556618518538\n\n# A Imgur API token (https://apidocs.imgur.com/?version=latest)\nImgur.token = "1234567890abcde"\n\n# A Steam Web API key (https://steamcommunity.com/dev/apikey)\nSteam.web_api_key = "123567890ABCDEF123567890ABCDEF12"\n\n# The Peertube instance you want to use for new video notifications\nPeertube.instance_url = "https://pt.steffo.eu"\n\n# The delay in seconds between two new video checks\nPeertube.feed_update_timeout = 300\n\n# The Funkwhale instance you want to use for the fw commands\nFunkwhale.instance_url = "https://fw.steffo.eu"\n\n# The id of the role that users should have to be displayed by default in cv\nCv.displayed_role_id = 424549048561958912\n\n# The max duration of a song downloaded with the play commands\nPlay.max_song_duration = 7230\n\n# The Telegram channel where matchmaking messages should be sent in\nMatchmaking.mm_chat_id = -1001204402796\n\n[Packs."royalpack"."steampowered"]\ntoken = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"\n\n[Packs."royalpack"."steampowered".updater]\nenabled = false\nperiod = 86400\ndelay = 1\ntarget = -1001153723135\n\n[Packs."royalpack"."dota".updater]\nenabled = true\nperiod = 86400\ndelay = 1\ntarget = -1001153723135\n\n[Packs."royalpack"."brawlhalla"]\ntoken = "1234567890ABCDEFGHJKLMNOPQRST"\n\n[Packs."royalpack"."brawlhalla".updater]\nenabled = true\nperiod = 86400\ndelay = 1\ntarget = -1001153723135\n\n[Packs."royalpack"."leagueoflegends"]\ntoken = "RGAPI-AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA"\nregion = "euw1"\n\n[Packs."royalpack"."leagueoflegends".updater]\nenabled = true\nperiod = 86400\ndelay = 1\ntarget = -1001153723135\n\n[Packs."royalpack"."osu"]\nclient_id = 123456789\nclient_secret = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"\n\n[Packs."royalpack"."osu".login]\nenabled = false\n\n[Packs."royalpack"."osu".updater]\nenabled = true\nperiod = 86400\ndelay = 5\ntarget = -1001153723135\n```',
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Steffo99/royalpack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

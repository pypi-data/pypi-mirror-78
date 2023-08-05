# `royalpack`

## Configuration

```toml
[Packs."royalpack"]

# The main Telegram group
Telegram.main_group_id = -1001153723135

# The main Discord channel
Discord.main_channel_id = 566023556618518538

# A Imgur API token (https://apidocs.imgur.com/?version=latest)
Imgur.token = "1234567890abcde"

# A Steam Web API key (https://steamcommunity.com/dev/apikey)
Steam.web_api_key = "123567890ABCDEF123567890ABCDEF12"

# The Peertube instance you want to use for new video notifications
Peertube.instance_url = "https://pt.steffo.eu"

# The delay in seconds between two new video checks
Peertube.feed_update_timeout = 300

# The Funkwhale instance you want to use for the fw commands
Funkwhale.instance_url = "https://fw.steffo.eu"

# The id of the role that users should have to be displayed by default in cv
Cv.displayed_role_id = 424549048561958912

# The max duration of a song downloaded with the play commands
Play.max_song_duration = 7230

# The Telegram channel where matchmaking messages should be sent in
Matchmaking.mm_chat_id = -1001204402796

[Packs."royalpack"."steampowered"]
token = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

[Packs."royalpack"."steampowered".updater]
enabled = false
period = 86400
delay = 1
target = -1001153723135

[Packs."royalpack"."dota".updater]
enabled = true
period = 86400
delay = 1
target = -1001153723135

[Packs."royalpack"."brawlhalla"]
token = "1234567890ABCDEFGHJKLMNOPQRST"

[Packs."royalpack"."brawlhalla".updater]
enabled = true
period = 86400
delay = 1
target = -1001153723135

[Packs."royalpack"."leagueoflegends"]
token = "RGAPI-AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA"
region = "euw1"

[Packs."royalpack"."leagueoflegends".updater]
enabled = true
period = 86400
delay = 1
target = -1001153723135

[Packs."royalpack"."osu"]
client_id = 123456789
client_secret = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

[Packs."royalpack"."osu".login]
enabled = false

[Packs."royalpack"."osu".updater]
enabled = true
period = 86400
delay = 5
target = -1001153723135
```
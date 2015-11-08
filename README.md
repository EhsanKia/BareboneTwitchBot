**BareboneTwitchBot**
===============

This is a bare minimal Python + Twisted bot for Twitch.
It sets up the basic IRC interactions, as well as support IRCv3 Tags,
and extra Twitch-API commands defined in the specs.

It does absolutely nothing else than connecting to a single channel
and logging various events such as messages and notices.

If you want a bot with slightly more meat and modular command support, check out [SimpleTwitchBot](https://github.com/EhsanKia/SimpleTwitchBot).

# Installation and usage
All you should need is Pyhton 2.7+ with [Twisted](https://twistedmatrix.com/trac/) installed.
You then copy this project in a folder, configure the bot and run `twitch_irc.py`.

#### Configuration:
Make sure to modify the following values in `bot.py`:
- `channel`: Twitch channel which the bot will run on
- `username`: The bot's Twitch user
- `oauth_key`: IRC oauth_key for the bot user (from [here](http://twitchapps.com/tmi/))

**Warning**: Make sure all channel and user names above are in lowercase.


# Code Overview

#####`twitch_irc.py`
This is the file that you run. It just starts up a Twisted IRC connection with the bot protocol.
The bot is currently built to only run in one channel, but you can still copy all the files over
to another folder with a different config and run it in parallel.

#####`bot.py`
Contains the bot IRC protocol. The main guts of the bot are here.

`privmsg` is where new messages arrive, `self.write(msg)` is what you use to talk.

# Contact
If you have any extra questions about the code, you can send me a PM on twitch: @ehsankia

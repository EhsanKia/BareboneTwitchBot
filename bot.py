from twisted.words.protocols import irc
import logging


class TwitchBot(irc.IRCClient, object):
    nickname = "ehsanbot"
    password = "oauth:100gqmdn3eg2qyaja8nhagkgoxomrp"
    channel = "#ehsankia"

    def signedOn(self):
        self.factory.wait_time = 1
        logging.warning("Signed on as {}".format(self.nickname))

        # Join channel
        self.sendLine("CAP REQ :twitch.tv/membership")
        self.sendLine("CAP REQ :twitch.tv/commands")
        self.sendLine("CAP REQ :twitch.tv/tags")
        self.join(self.channel)

    def joined(self, channel):
        logging.warning("Joined %s" % channel)

    def privmsg(self, user, channel, msg):
        # Extract twitch name
        name = user.split('!', 1)[0].lower()

        # Log the message
        logging.info("{}: {}".format(name, msg))

    def parsemsg(self, s):
        """Breaks a message from an IRC server into its prefix, command, and arguments."""
        tags, prefix, trailing = {}, '', []
        if s[0] == '@':
            tags_str, s = s[1:].split(' ', 1)
            tag_list = tags_str.split(';')
            tags = dict(t.split('=') for t in tag_list)
        if s[0] == ':':
            prefix, s = s[1:].split(' ', 1)
        if s.find(' :') != -1:
            s, trailing = s.split(' :', 1)
            args = s.split()
            args.append(trailing)
        else:
            args = s.split()
        command = args.pop(0).lower()
        return tags, prefix, command, args

    def lineReceived(self, line):
        '''Parse IRC line'''
        # First, we check for any custom twitch commands
        tags, prefix, cmd, args = self.parsemsg(line)
        if cmd == "hosttarget":
            self.hostTarget(*args)
        elif cmd == "clearchat":
            self.clearChat(*args)
        elif cmd == "notice":
            self.notice(tags, args)

        # Remove tag information
        if line[0] == "@":
            line = line.split(' ', 1)[1]

        # Then we let IRCClient handle the rest
        super(TwitchBot, self).lineReceived(line)

    def hostTarget(self, channel, target):
        '''Track and update hosting status'''
        target = target.split(' ')[0]
        if target == "-":
            logging.warning("Exited host mode")
        else:
            logging.warning("Now hosting {}".format(target))

    def clearChat(self, channel, target=None):
        '''Log chat clear notices'''
        if target:
            logging.warning("{} was timed out".format(target))
        else:
            logging.warning("chat was cleared")

    def notice(self, tags, args):
        '''Log all chat mode changes'''
        if "msg-id" not in tags:
            return
        logging.warning(tags['msg-id'])

    def write(self, msg):
        '''Send message to channel and log it'''
        self.msg(self.channel, msg)
        logging.info("{}: {}".format(self.nickname, msg))

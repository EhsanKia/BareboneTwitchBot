from twisted.internet import protocol, reactor
import logging
import time
import bot


class BotFactory(protocol.ClientFactory):
    protocol = bot.TwitchBot
    wait_time = 1

    def clientConnectionLost(self, connector, reason):
        logging.error("Lost connection, reconnecting")
        self.protocol = reload(bot).TwitchBot
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        msg = "Could not connect, retrying in {}s"
        logging.warning(msg.format(self.wait_time))
        time.sleep(self.wait_time)
        self.wait_time = min(512, self.wait_time * 2)
        connector.connect()


if __name__ == "__main__":
    reactor.connectTCP('irc.twitch.tv', 6667, BotFactory())
    reactor.run()

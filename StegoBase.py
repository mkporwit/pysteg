import abc
import base64
import pystegcfg


class StegoBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def encode(self, carrier, payload, tiling):
        """Encode the provided payload into the carrier, with appropriate tiling."""
        return

    @abc.abstractmethod
    def decode(self, carrier):
        """Decode the payload from the carrier and return a bitmask of the payload(s)."""
        return

    def listToText(msgList):
        nElem = len(msgList)
        ret = ""
        failedCount = 0

        if(nElem > 1):
            ret += "Found {0} unique messages. Will print them all\n".format(nElem)
            for (encMsg, count) in msgList:
                try:
                    if pystegcfg.encoding is "base64":
                        ret += "[{0}]: {1}\n".format(base64.b64decode(encMsg), count)
                    elif pystegcfg.encoding is "none":
                        ret += "[{0}]: {1}\n".format(encMsg, count)

                except TypeError:
                    failedCount += 1
        elif(nElem is 1):
            (encMsg, count) = msgList[0]
            try:
                if pystegcfg.encoding is "base64":
                    ret += "[{0}]".format(base64.b64decode(encMsg))
                elif pystegcfg.encoding is "none":
                    ret += "[{0}]".format(encMsg)

            except TypeError:
                    failedCount += 1

        if failedCount > 0:
            ret += "{0} of {1} failed to decode".format(failedCount, nElem)

        return ret

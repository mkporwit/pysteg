import mask
import text2bits as tb
import StegoException
import base64
import collections
import pystegcfg


def encode(data, msg):
    if not pystegcfg.encoding in pystegcfg.encodingopts:
        raise ValueError("Encoding [{0}] is invalid. Can only be one of {1}".format(pystegcfg.encoding, pystegcfg.encodingopts))

    if pystegcfg.encoding is "base64":
        encMsg = base64.b64encode(msg) + pystegcfg.delim
    elif pystegcfg.encoding is "none":
        encMsg = msg + pystegcfg.delim

    encMask = tb.text2uint8mask(encMsg)
    if(data.size < len(encMsg)):
        raise StegoException.EncodeError("Data size [{0}] is too small to fit encoded message of size [{1}]".format(data.size, len(encMask)))

    encData = mask.applyLSB(data, encMask)

    return encData


def decode(data):
    if not pystegcfg.encoding in pystegcfg.encodingopts:
        raise ValueError("Encoding [{0}] is invalid. Can only be one of {1}".format(pystegcfg.encoding, pystegcfg.encodingopts))

    encMask = mask.extractLSB(data)
    encMsg = tb.uint8mask2text(encMask)
    # Extract all instances of the encoded message from the encMsg  string
    encMsgList = encMsg.split(pystegcfg.delim)
    # remove any empty array elements
    encMsgList = filter(None, encMsgList)

    encMsgListCounted = collections.Counter(encMsgList).most_common()
    nElem = len(encMsgListCounted)
    if(nElem < 1):
        raise StegoException.DecodeError("No message to decode")

    return encMsgListCounted


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

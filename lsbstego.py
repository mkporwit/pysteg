import mask
import text2bits as tb
import StegoException
import base64
import collections


def encode(data, msg, delim):
    encMsg = base64.b64encode(msg) + delim
    encMask = tb.text2uint8mask(encMsg)
    if(data.size < len(encMsg)):
        raise StegoException.EncodeError("Data size [{0}] is too small to fit encoded message of size [{1}]".format(data.size, len(encMask)))

    encData = mask.applyLSB(data, encMask)

    return encData


def decode(data, delim):
    encMask = mask.extractLSB(data)
    encMsg = tb.uint8mask2text(encMask)
    # Extract all instances of the encoded message from the encMsg  string
    encMsgList = encMsg.split(delim)
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
                ret += "[{0}]: {1}\n".format(base64.b64decode(encMsg), count)
            except TypeError:
                failedCount += 1
    elif(nElem is 1):
        (encMsg, count) = msgList[0]
        try:
            ret += "[{0}]".format(base64.b64decode(encMsg))
        except TypeError:
                failedCount += 1

    if failedCount > 0:
        ret += "{0} of {1} failed to decode".format(failedCount, nElem)

    return ret

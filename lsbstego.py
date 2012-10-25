import mask
import text2bits as tb
import StegoException
import base64
import collections


def encode(data, msg, delim):
    encMsg = base64.b64encode(msg) + delim
    encMask = tb.text2uint8mask(encMsg)
    if(data.size < encMsg.size):
        raise StegoException.EncodeError("Data size [{0}] is too small to fit encoded message of size [{1}]".format(data.size, encMask.size))

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
    elif(nElem > 1):
        print "Found {0} unique messages. Will print them all.".format(nElem)
        for (encMsg, count) in encMsgListCounted:
            print "[{0}]: {1}".format(base64.b64decode(encMsg), count)
    else:
        (encMsg, count) = encMsgListCounted.most_common(1)
        print "[{0}]".format(base64.b64decode(encMsg))

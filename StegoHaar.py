import mask
import text2bits as tb
import base64
import collections
import pystegcfg
import StegoException
from StegoBase import StegoBase


class StegoHaar(StegoBase):
    def encode(data, msg, tiling):
        if not pystegcfg.encoding in pystegcfg.encodingopts:
            raise ValueError("Encoding [{0}] is invalid. Can only be one of {1}".format(pystegcfg.encoding, pystegcfg.encodingopts))

        if pystegcfg.encoding is "base64":
            encMsg = base64.b64encode(msg) + pystegcfg.delim
        elif pystegcfg.encoding is "none":
            encMsg = msg + pystegcfg.delim

        encMask = tb.text2uint8mask(encMsg)
        if(data.size < len(encMsg)):
            raise StegoException.EncodeError("Data size [{0}] is too small to fit encoded message of size [{1}]".format(data.size, len(encMask)))

        encData = mask.applyHaar(data, encMask)

        return encData

    def decode(data):
        if not pystegcfg.encoding in pystegcfg.encodingopts:
            raise ValueError("Encoding [{0}] is invalid. Can only be one of {1}".format(pystegcfg.encoding, pystegcfg.encodingopts))

        encMask = mask.extractHaar(data)
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

if __name__ == '__main__':
    print 'Subclass:', issubclass(StegoHaar, StegoBase)
    print 'Instance:', isinstance(StegoHaar(), StegoBase)

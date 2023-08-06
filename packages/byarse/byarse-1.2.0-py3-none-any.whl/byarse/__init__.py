import pickle
import datetime
import struct
import math


def int_from_bytes(b):
    return int.from_bytes(b, 'big', signed=True)


def floattobytes(f):
    return struct.pack("d", f)


def bytestofloat(b):
    return struct.unpack("d", b)[0]


def dtfromtimestamp(b):
    return datetime.datetime.fromtimestamp(bytestofloat(b))


class Pickle:
    def __init__(self, obj):
        """Object for byarse to pickle and depickle"""
        self.obj = obj


_typeref = {
    b'B':bytes,
    b'I':int_from_bytes,
    b'F':bytestofloat,
    b'S':str,
    b'P':pickle.loads,
    b'D':dtfromtimestamp
}


def arg_as_bytes(arg):
    if type(arg) is int:
        return int(arg).to_bytes(math.ceil((arg.bit_length())/8), 'big', signed=True)
    elif type(arg) is float:
        return floattobytes(float(arg))
    elif type(arg) is str:
        return arg.encode()
    elif type(arg) is Pickle:
        return pickle.dumps(arg.obj)
    elif type(arg) is datetime.datetime:
        ts = arg.replace(tzinfo=datetime.timezone.utc).timestamp()
        return floattobytes(float(ts))
    
    return arg



class BAS:
    def __init__(self, **kw):
        """
        Bytes Argument Serializer and Deserializer

        Keyword Arguments:
            - safe [bool]: Prevent from parsing pickled type. (Default: True)
        """
        self.safe = bool(kw.get('safe', True))
        
        
    def s(self, args):
        """Serialize arguments"""
        r = b''
        
        for arg in args:
            r += type(arg).__name__[0].encode().upper() # 1 Byte Type Representation (ex. "B" for bytes)
            arg = arg_as_bytes(arg) # Argument converted to bytes
            r += len(arg).to_bytes(8, 'big') # Length of argument
            r += arg # Argument
        
        return r
        

    def u(self, s, limit=-1):
        """Deserialize arguments"""
        args = []
        pos = 0

        while pos <= len(s)-1 and len(args) != limit: # Read until complete or until at limit
            # Type Representation (B, I, F, ...)
            t = _typeref[bytes([s[pos]])]
    
            pos += 1

            length = int.from_bytes(s[pos:(pos+8)], 'big') # Length of following argument

            pos += 8

            if t is str:
                args.append(s[pos:(pos+length)].decode()) # Decode argument to string
            else:
                # Enforce safe mode
                if t is pickle.loads and self.safe:
                    raise TypeError("Pickle argument passed in safe mode.")
        
                args.append(t(s[pos:(pos+length)]))

            pos += length

        return args

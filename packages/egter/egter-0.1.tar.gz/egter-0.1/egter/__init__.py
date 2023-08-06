import random
import binascii

version = '0.1'


class EHash:
    """
    (C) Egor Ternovoy. 2020

    !!! NOT SO SAFE! It is possible to reverse calculate source bytes from hash! !!!

    Uses library random

    Usage:
        import egter

        hash = egter.EHash(b'some bytes', lenght=32, iterations=100)  # lenght - bytes count

        print(hash) # equal to hexdigest method
        # 90b0f287805156865bfebbf93eac3328ab0e9bcbb82dfcc9d5f88d6d41524766

        print(hash.digest()) # bytes
        # b'\x90\xb0\xf2\x87\x80QV\x86[\xfe\xbb\xf9>\xac3(\xab\x0e\x9b\xcb\xb8-\xfc\xc9\xd5\xf8\x8dmARGf'

        print(hash.hexdigest())
        # 90b0f287805156865bfebbf93eac3328ab0e9bcbb82dfcc9d5f88d6d41524766

        print(hash.intdigest())
        # 65445689155113512790458496256639542022557958647760937310771143133228635932518

        hash.update(b'add bytes to hash')
        print(hash.hexdigest())
        # 591822f89a114ede35c8ac4a4ebeda6952fd6f4114a9434ebe27b1b8fc6b0d2a

        # set custom seed
        hash.generate(b'some seed')
        print(hash.hexdigest())
        # a2c401e4e18b0ebda141fd63da4a0efbc9253b9d204e6c24381b9bd45ec4abc1

        hash2 = egter.EHash(int) # equal to egter.EHash('<class 'int'>')
        print(hash)
        # a7eb7705b8a37e77df4a48882584b4bcfa20377b305bdae586784636be9ba255

        custom_hash = egter.EHash('custom hash', custom=(1, 2, 3), custom_type=str) # custom_type = str|bytes,
                                                                                           #custom = iterable type
        print(custom_hash.customdigest())
        # 11321321121122112121111133122213
    """

    def __init__(self, text, lenght=32, iterations=100, custom=(1, 2, 3), custom_type=str):
        """Creates EHash object"""
        if not isinstance(text, (str, bytes, bytearray)):
            text = str(text)
        if isinstance(text, str):
            text = text.encode()
        self.custom = custom
        self.custom_type = custom_type
        self.bytes = b''
        self.lenght = lenght
        self.iterations = iterations
        for i in range(iterations):
            for letter in text:
                self.generate(letter)

    def generate(self, seed):
        """Generating hash"""
        random.seed(self.bytes + bytearray(seed))
        self.bytes = bytes(random.choices(range(256), k=self.lenght))

    def update(self, text):
        """Update existing hash"""
        if not isinstance(text, (str, bytes, bytearray)):
            text = str(text)
        if isinstance(text, str):
            text = text.encode()
        for i in range(self.iterations):
            for letter in text:
                self.generate(letter)

    def digest(self):
        """Return BYTES"""
        return self.bytes

    def hexdigest(self):
        """Return HEX"""
        return binascii.hexlify(self.bytes).decode()

    def intdigest(self):
        """return INT"""
        return int.from_bytes(self.bytes, byteorder='big')

    def customdigest(self):
        """return custom letters hash"""
        return self.custom_type('').join([self.custom_type(i) for i in random.choices(self.custom, k=self.lenght)])

    def __str__(self):
        return binascii.hexlify(self.bytes).decode()

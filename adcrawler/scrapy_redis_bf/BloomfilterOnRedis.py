# encoding=utf-8
import logging


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    logger = logging.getLogger(__name__)

    def __init__(self, server, key, blockNum=1):
        self.logger.info(' BloomFilter Begin '.center(80, '-'))

        self.bit_size = 1 << 29  # the max length of String in Redis is 512M，now set 64M,m=2^29=536,870,912,n=24,000,000
        # self.seeds = [5, 7, 11, 13, 31]
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.server = server
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        if not str_input:
            # self.logger.info(' BloomFilter: Not str_input '.center(80, '-'))
            return False
        ret = True

        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)

        # self.logger.info(str(' BloomFilter: Check str_input = ' + str_input).center(80, '-'))
        # self.logger.info(str(' BloomFilter: ret = ' + str(ret) + ' ').center(80, '-'))
        return ret

    def insert(self, str_input):
        # self.logger.info(str(' BloomFilter: Insert str_input = ' + str_input).center(80, '-'))
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)

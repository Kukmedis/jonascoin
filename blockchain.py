import hashlib
import itertools as it
from datetime import datetime

BLOCK_GENERATION_INTERVAL = 10

DIFFICULTY_ADJUSTMENT_INTERVAL = 10


class Block:

    def __init__(self, index, previous_hash, calculated_hash, data, difficulty, nonce, timestamp):
        self.index = index
        self.hash = calculated_hash
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.nonce = nonce

    @classmethod
    def create(cls, index, previous_hash, data, difficulty, nonce, timestamp):
        calculated_hash = hashlib.sha256(
            (str(index) + previous_hash + str(data) + str(nonce) + str(difficulty) + str(timestamp))
            .encode('utf-8')).hexdigest()
        return cls(index, previous_hash, calculated_hash, data, difficulty, nonce, timestamp)

    def __eq__(self, o):
        return (self.index == o.index) \
               and (self.hash == o.hash) \
               and (self.previous_hash == o.previous_hash) \
               and (self.data == o.data) \
               and (self.timestamp == o.timestamp)


class Blockchain:
    def __init__(self):
        self.blockchain = [genesis_block]

    def add_block(self, data, difficulty, nonce):
        last_block = self.blockchain[-1]
        timestamp = int(datetime.now().timestamp() * 1000)
        new_block = Block.create(last_block.index + 1, last_block.hash, str(data), str(difficulty), str(nonce),
                                 str(timestamp))
        self.blockchain.append(new_block)

    def replace(self, new_bc):
        current_cumulative_difficulty = sum(pow(2, block.difficulty) for block in self.blockchain)
        new_cumulative_difficulty = sum(pow(2, block.difficulty) for block in new_bc.blockchain)
        if new_cumulative_difficulty > current_cumulative_difficulty:
            self.blockchain = new_bc

    def get_difficulty(self):
        last_block = self.blockchain[-1]
        if last_block.index % DIFFICULTY_ADJUSTMENT_INTERVAL == 0 and last_block.index != 0:
            previous_adjusted_block = self.blockchain[len(self.blockchain) - DIFFICULTY_ADJUSTMENT_INTERVAL]
            time_expected = BLOCK_GENERATION_INTERVAL * DIFFICULTY_ADJUSTMENT_INTERVAL
            time_taken = last_block.timestamp - previous_adjusted_block.timestamp
            if time_taken < time_expected / 2:
                return previous_adjusted_block.difficulty + 1
            elif time_taken > time_expected * 2:
                return previous_adjusted_block.difficulty - 1
            else:
                return previous_adjusted_block.difficulty
        else:
            return last_block.difficulty


genesis_block = Block(0, "", "ac34557f94c70cc7faff7d25f59907dac174e2d7d776bd60f069f682f26f7626",
                      "jonascoin Genesis Block", 0, 0, 1515186462990)


def is_new_block_valid(previous_block, new_block):
    return (new_block.index == previous_block.index + 1) \
           and (new_block.previous_hash == previous_block.hash) \
           and (hashlib.sha256((str(new_block.index) + str(new_block.previous_hash)
                                + str(new_block.data) + str(new_block.nonce) + str(new_block.difficulty)
                                + str(new_block.timestamp)).encode('utf-8')).hexdigest()
                == new_block.hash) \
           and hash_matches_difficulty(new_block.hash, new_block.difficulty) \
           and timestamp_valid(previous_block, new_block)


def hash_matches_difficulty(hash_to_check, difficulty):
    return 256 - (int(hash_to_check, 16)).bit_length() >= difficulty


def timestamp_valid(previous_block, new_block):
    return previous_block.timestamp - 60000 < new_block.timestamp \
           and new_block.timestamp - 60000 < int(datetime.now().timestamp() * 1000)


def is_chain_valid(blockchain):
    return blockchain and blockchain[0] == genesis_block \
           and all(map(lambda x_y: is_new_block_valid(x_y[0], x_y[1]), pairwise(blockchain)))


def pairwise(iterable):
    a, b = it.tee(iterable)
    next(b, None)
    return zip(a, b)

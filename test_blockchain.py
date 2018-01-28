import unittest
import blockchain
from unittest.mock import patch
from datetime import datetime
from blockchain import Blockchain, Block, hash_matches_difficulty


class BlockchainTest(unittest.TestCase):

    @patch('blockchain.datetime')
    def test_add_new_block(self, mock_date):
        mock_date.now.return_value = datetime.fromtimestamp(1515193204)
        bc = Blockchain()
        bc.add_block("TEST DATA 1", 0, 0)
        added_block = bc.blockchain[1]
        self.assertEqual("ac34557f94c70cc7faff7d25f59907dac174e2d7d776bd60f069f682f26f7626", added_block.previous_hash)
        self.assertEqual(1, added_block.index)
        self.assertEqual("TEST DATA 1", added_block.data)
        self.assertEqual("836f04540c1972054224a4c476386664d2b5c65d57fbf04033ff5385c3886faa", added_block.hash)

    def test_is_chain_valid(self):
        bc = [
            Block(0, "", "ac34557f94c70cc7faff7d25f59907dac174e2d7d776bd60f069f682f26f7626",
                  "jonascoin Genesis Block", 0, 0, 1515186462990),
            Block(1, "ac34557f94c70cc7faff7d25f59907dac174e2d7d776bd60f069f682f26f7626",
                  "836f04540c1972054224a4c476386664d2b5c65d57fbf04033ff5385c3886faa",
                  "TEST DATA 1", 0, 0, 1515193204000),
            Block(2, "836f04540c1972054224a4c476386664d2b5c65d57fbf04033ff5385c3886faa",
                  "0de6943a9864e08d3981998b2f909227608a0161929ca17cee6b9fcca6b639f8",
                  "TEST DATA 2", 0, 0, 1515193205000)
        ]
        self.assertTrue(blockchain.is_chain_valid(bc))

    def test_hash_matches_difficulty(self):
        self.assertTrue(hash_matches_difficulty("6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b", 1))
        self.assertTrue(hash_matches_difficulty("ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d", 0))
        self.assertTrue(hash_matches_difficulty("1121cfccd5913f0a63fec40a6ffd44ea64f9dc135c66634ba001d10bcf4302a2", 2))
        self.assertTrue(hash_matches_difficulty("1121cfccd5913f0a63fec40a6ffd44ea64f9dc135c66634ba001d10bcf4302a2", 3))
        self.assertFalse(hash_matches_difficulty("1121cfccd5913f0a63fec40a6ffd44ea64f9dc135c66634ba001d10bcf4302a2", 4))


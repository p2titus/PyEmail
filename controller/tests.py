import unittest
import os
import json


class LoadKeysTest(unittest.TestCase):
    prod_keys = None
    __KEYS_FNAME = 'test.json'
    __TEST_KEYS = LoadKeysTest.__gen_keys()

    def tearDown(self) -> None:
        # we return the prod keys after a test
        # although if you're saving your prod keys in a file called test.json, you kinda deserve it
        if self.prod_keys is not None:
            fname = self.__KEYS_FNAME
            if os.path.exists(fname):
                os.remove(fname)
            permissions = 'w'
            with open(fname, permissions) as f:
                json.dump(self.prod_keys, f)

    @staticmethod
    def __gen_keys():
        return dict(test=dict(addr="test", type="example.com", keys="testpwd"))

    @classmethod
    def setUp(cls) -> None:
        def_ks = cls.__TEST_KEYS
        fname = cls.__KEYS_FNAME
        perm = 'rw'
        with open(fname, perm) as f:
            if os.path.exists(fname):
                cls.prod_keys = json.load(f)
            json.dumps(def_ks)

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()

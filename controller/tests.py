import unittest
import os
import json


class LoadKeysTest(unittest.TestCase):
    from load_keys import load_account_details
    prod_keys = None
    __KEYS_FNAME = 'test.json'
    __TEST_KEYS: (str, str, str) = None

    @classmethod
    def tearDownClass(cls) -> None:
        # we return the prod keys after a test
        # although if you're saving your prod keys in a file called test.json, you kinda deserve it
        if cls.prod_keys is not None:
            fname = cls.__KEYS_FNAME
            if os.path.exists(fname):
                os.remove(fname)
            if cls.prod_keys is not None:
                with open(fname, 'w') as f:
                    json.dump(cls.prod_keys, f)

    @staticmethod
    def __gen_keys():
        # return 'test', 'example.com', 'testpwd'
        return dict(test=dict(addr="test", type="example.com", keys="testpwd"))

    @classmethod
    def setUpClass(cls) -> None:
        def_ks = cls.__gen_keys()
        cls.__TEST_KEYS = cls.__extract_keys(def_ks)
        fname = '../%s' % cls.__KEYS_FNAME
        if os.path.exists(fname) and os.stat(fname).st_size > 0:
            with open(fname, 'r') as f:
                cls.prod_keys = json.load(f)
        with open(fname, 'w') as f:
            json.dump(def_ks, f, indent=4)
        print(cls.__TEST_KEYS)
        print(cls.__KEYS_FNAME)

    @staticmethod
    def __extract_keys(ds):
        acc = []
        if len(ds) > 1:
            for d in ds:
                acc.append((d['addr'], d['type'], d['keys']))
        elif len(ds) == 1:
            xs = ds['test']  # cheesed it
            acc = [(xs['addr'], xs['type'], xs['keys'])]
        return acc

    def test_basic(self):
        ks = self.load_account_details(keys_file_name=self.__KEYS_FNAME)
        self.assertEqual(ks, self.__TEST_KEYS)


if __name__ == '__main__':
    unittest.main()

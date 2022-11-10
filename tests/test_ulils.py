import json
import os
from unittest import TestCase
from uuid import uuid4

from neo3 import wallet as neo3_wallet

from neofs_testlib.utils import converters, wallet


class TestUtils(TestCase):
    def test_converters_str_to_ascii_hex(self):
        source_str = ""
        result_str = ""
        self.assertEqual(converters.str_to_ascii_hex(source_str), result_str)

        source_str = '"test_data" f0r ^convert*'
        result_str = "22746573745f646174612220663072205e636f6e766572742a"
        self.assertEqual(converters.str_to_ascii_hex(source_str), result_str)

        source_str = ""
        result_bytes = b""
        self.assertEqual(converters.ascii_hex_to_str(source_str), result_bytes)

        source_str = "22746573745f646174612220663072205e636f6e766572742a"
        result_bytes = b'"test_data" f0r ^convert*'
        self.assertEqual(converters.ascii_hex_to_str(source_str), result_bytes)

    def test_process_b64_bytearray_reverse(self):
        source_str = ""
        result_bytes = b""
        self.assertEqual(converters.process_b64_bytearray_reverse(source_str), result_bytes)

        source_str = "InRlc3RfZGF0YSIgZjByIF5jb252ZXJ0Kg=="
        result_bytes = b"2a747265766e6f635e207230662022617461645f7473657422"
        self.assertEqual(converters.process_b64_bytearray_reverse(source_str), result_bytes)

    def test_process_b64_bytearray(self):
        source_str = ""
        result_bytes = b""
        self.assertEqual(converters.process_b64_bytearray(source_str), result_bytes)

        source_str = "InRlc3RfZGF0YSIgZjByIF5jb252ZXJ0Kg=="
        result_bytes = b"22746573745f646174612220663072205e636f6e766572742a"
        self.assertEqual(converters.process_b64_bytearray(source_str), result_bytes)

    def test_contract_hash_to_address(self):
        source_str = "d01a381aae45f1ed181db9d554cc5ccc69c69f4e"
        result_str = "NT5hJ5peVmvYdZCsFKUM5MTcEGw5TB4k89"
        self.assertEqual(converters.contract_hash_to_address(source_str), result_str)

    def test_init_wallet(self):
        wallet_file_path = f"{str(uuid4())}.json"
        for password in ("", "password"):
            wrong_password = "wrong_password"
            wallet.init_wallet(wallet_file_path, password)
            self.assertTrue(os.path.exists(wallet_file_path))
            with open(wallet_file_path, "r") as wallet_file:
                neo3_wallet.Wallet.from_json(json.load(wallet_file), password=password)
            with self.assertRaises(Exception):
                neo3_wallet.Wallet.from_json(json.load(wallet_file), password=wrong_password)
            os.unlink(wallet_file_path)

    def test_get_last_address_from_wallet(self):
        wallet_file_path = f"{str(uuid4())}.json"
        for password in ("", "password"):
            wallet.init_wallet(wallet_file_path, password)
            with open(wallet_file_path, "r") as wallet_file:
                wlt = neo3_wallet.Wallet.from_json(json.load(wallet_file), password=password)
            last_address = wlt.accounts[-1].address
            self.assertEqual(
                wallet.get_last_address_from_wallet(wallet_file_path, password), last_address
            )
            os.unlink(wallet_file_path)

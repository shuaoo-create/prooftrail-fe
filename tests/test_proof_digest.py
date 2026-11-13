import unittest
from scripts.proof_digest import digest_bytes


class DigestTests(unittest.TestCase):
    def test_repeatable(self):
        salt = bytes.fromhex('00' * 32)
        self.assertEqual(digest_bytes(b'example', salt), digest_bytes(b'example', salt))

    def test_content_change(self):
        salt = bytes.fromhex('00' * 32)
        self.assertNotEqual(digest_bytes(b'example', salt), digest_bytes(b'Example', salt))

    def test_salt_change(self):
        self.assertNotEqual(digest_bytes(b'example', bytes(32)), digest_bytes(b'example', bytes([1]) * 32))

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            digest_bytes(b'', bytes(32))

    def test_wrong_length_rejected(self):
        with self.assertRaises(ValueError):
            digest_bytes(b'example', bytes(16))


if __name__ == '__main__':
    unittest.main()

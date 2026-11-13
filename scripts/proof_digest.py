#!/usr/bin/env python3
"""Compute a salted ProofTrail commitment; no content is uploaded."""
import argparse
import hashlib
from pathlib import Path

DOMAIN = b"prooftrail-fe-v1\x00"


def digest_bytes(content: bytes, salt: bytes) -> str:
    if len(salt) != 32:
        raise ValueError("salt must be exactly 32 bytes")
    if not content:
        raise ValueError("content must not be empty")
    preimage = DOMAIN + salt + len(content).to_bytes(8, "big") + content
    return "0x" + hashlib.sha256(preimage).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--salt-hex", required=True, help="64 hex digits from a local random generator")
    args = parser.parse_args()
    print(digest_bytes(args.file.read_bytes(), bytes.fromhex(args.salt_hex)))


if __name__ == "__main__":
    main()

# ProofTrail Fe — versioned AI disclosure commitments

> **Contest prototype (locally verified Fe build)** · Fe Builders Challenge 2026 · MIT · no real-world deployment

**One-sentence pitch:** ProofTrail lets creators commit salted content hashes and AI-assistance declarations with a versioned, author-controlled finalization step, without publishing their manuscripts.

## Why

A competition entrant may need to show **which version** of a work and AI-use disclosure existed at a point in an editing workflow. An uneditable registry is too rigid for drafts; an editable record loses history. ProofTrail offers both: per-author append-only numbered commitments, then an irreversible freeze. The caller's EVM address is the account namespace, not an identity guarantee.

## Fe-specific contribution

The core registry is implemented in Fe 26.6.0 (5b3f96a): `msg` receive interfaces with Solidity-compatible selectors, declared `Ctx` and mutable `Log` effects, typed composite-key `StorageMap<(Address,u256),u256>`, explicit handler access with `uses`, and event emission. Python is only an optional *offchain* hash preparation script.

## Design

- `Commit(digest, ai_mode)`: increments the caller's version; preserves old versions; writes `digestAt` and `modeAt`, emits `ProofCommitted`.
- `Freeze()`: irreversible per-address finalization, emits `ProofFinalized`. Rejects missing prior commits.
- `VersionOf`, `DigestAt`, `ModeAt`, `IsFrozen`: public verification queries. Unknown version returns zero.
- `ai_mode` is a coarse self-declaration: `0` = no AI declared, `1` = AI-assisted, `2` = AI-led. It is **not** a verified percentage.
- Salted SHA-256 commitment format `SHA256(UTF-8("prooftrail-fe-v1") || 0x00 || salt32 || uint64be(len(content)) || raw_content)`. Here `0x00` is one NUL byte.

## Reproducible build and test

Install Fe `v26.6.0`. The verified compiler reports `fe 26.6.0 (5b3f96a)`. See [official Fe installation](https://fe-lang.org/getting-started/installation/).

```bash
fe --version
fe check
fe fmt --check
fe test
fe build
```

`src/tests.fe` contains seven EVM tests: initial commit, historical versions, freeze, and four negative cases. All seven passed on November 13, 2026 UTC under Fe 26.6.0. `fe check`, `fe fmt --check`, and `fe build` also completed successfully. See `validation/RESULTS.json` and the captured logs for exact commands, exit codes, timestamps and outputs. CI is configured for the same version; inspect the repository Actions page for current remote results.

Offchain digest helper can be tested independently:

```bash
python -m unittest discover -s tests -v
# Supply a 32-byte salt from your own random generator; this example is a public test salt only:
python scripts/proof_digest.py fixtures/example.txt --salt-hex "$(printf '00%.0s' {1..32})"
```

For real use, choose a fresh 32-byte random salt and retain it privately with the exact document bytes. A random salt protects against straightforward guesses of short, predictable plaintext. Do **not** reuse the zero test salt for sensitive material.

## Judging demo (local, without funds)

1. Run `fe test`. It deploys `ProofTrail` inside the local EVM test runner, without mainnet or funds.
2. Commit a salted hash with `ai_mode=2`; query version 1.
3. Modify the document, hash again, commit version 2; read both versioned hashes.
4. Finalize; verify `IsFrozen` and the revert on further `Commit`.

## Limitations and threat model

- A hash commitment does **not prove original authorship**, the truth of an AI disclosure, who controlled a wallet, or when the original file was created; it only attests a value was submitted by an address in a transaction at that blockchain time.
- Source prompt/output logs are not retained onchain. Entrants must separately retain the real logs and comply with each contest's rules.
- Plaintext is never sent by this contract, but onchain data is public. A weak or public salt can still allow guessing attacks.
- `Freeze` cannot be undone, even if keys are lost or data is incorrect. No recovery/transfer function is included.
- No audit, real deployment, gas benchmark, security guarantee or prize-entry acceptance yet. Passing local tests establish only the tested cases.
- This project must not be deployed to mainnet without extensive independent review.

## Contest readiness

Source created November 5, 2026, within the build window. Registration was confirmed by the organizer on November 13, 2026 at 18:41:48 UTC; project ID **FE-056**. The finished project has **not** been submitted. This public repository contains the review source. Final submission uses an exact full commit SHA through the private organizer submission link.

## Rights / acknowledgments

This project contains original contest-draft logic, written with AI assistance. The original contract logic compiled unchanged; the source was formatted with the official formatter and tested locally on November 13, 2026 UTC. It draws on the [Fe Guide](https://fe-lang.org/) and [official starter](https://github.com/fe-lang/builders-challenge-starter) to understand Fe syntax; starter Fe source was not copied verbatim. Any external components remain under their own licenses. The newly created files here are released under MIT.

## Verification update — 2026-11-13 18:40 UTC

Restored the original private draft archive, installed the official free Fe 26.6.0 Linux x86_64 release in an isolated local directory, and ran the original tests. No new contract behavior was added. The compiler runs locally; no account, wallet, paid API, gas, or public publication was used. The official registration was subsequently confirmed as FE-056. Final submission remains pending. Private submission credentials are stored separately.

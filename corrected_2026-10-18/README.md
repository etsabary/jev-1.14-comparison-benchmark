# Active corrected text decision bank

This is the active 1,136-question benchmark as of October 18, 2026. It replaces two ambiguous procedure variants with clarified final-state questions. The other 1,134 questions and responses per model are unchanged. There are 36 complete configurations and 40,896 first-attempt cases.

- `questions_1136.csv`, `item_metadata.csv` and `selection_manifest.json` define the active inputs and relationships. Both retired original item IDs are absent from this bank.
- `summary.json` and `family_comparison.csv` contain the recomputed aggregates. Scores use first attempts. Latency pools all 1,136 selected first attempts; cost includes their permitted recoveries.
- `replacement_evidence/` preserves the exact frozen dispatch plan, 72 sanitized new attempts, model metadata, route overrides and bound completion receipts. `replacement_attempts.jsonl` is a convenient aggregate of those same attempts.
- `source_manifest.json` links the unchanged original capture ledgers and their checksums. Selecting their 1,134 retained items plus the two new items reconstructs each active configuration.
- `correction_receipt.json` summarizes the audit, replacement verification, deltas, unavailable original Nimble v4 and removed-call overhead. `routes.json` labels the two provider changes.

`checksums.json` seals the exact imported evidence export. `release_checksums.json` additionally seals the current presentation, graphics and validation sources. Earlier capture seals remain unchanged. Earlier question files outside this folder are capture references, not the active bank.

Run `python3 validate_corrected_release.py` from the repository root for the self-contained, key-free check. It reconstructs selected records and verifies timing, cost, coverage, source hashes and aggregate consistency. It does not reproduce correctness without the private key. Before export, the offline assembler reproduced all 40 original primary and eventual scores with that external frozen key, then recomputed the corrected aggregates.

The `source/` assembly and export files are source snapshots for provenance, not a standalone inference package. They retain dependencies on the private audit controller. The public validator in that folder is self-contained. No private answer key, verifier answer traces or item-level correctness is published.

"""Bind public data, analysis and figure bytes after reviewed regeneration."""
from pathlib import Path
import json
from analyze import file_hash
root=Path(__file__).resolve().parent
paths=sorted(p for folder in ["data","analysis","figures"] for p in (root/folder).glob("*") if p.is_file() and p.name!="checksums.json")
(root/"data/checksums.json").write_text(json.dumps({p.relative_to(root).as_posix():file_hash(p) for p in paths},indent=2)+"\n")
print(f"Recorded {len(paths)} artifact hashes")

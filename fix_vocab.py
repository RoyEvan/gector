import shutil
from pathlib import Path
from datetime import datetime

VOCAB_DIR = Path("data/output_vocabulary")
BACKUP_DIR = Path("vocab_backup")
DTAGS = VOCAB_DIR / "d_tags.txt"
LABELS = VOCAB_DIR / "labels.txt"
NON_PADDED = VOCAB_DIR / "non_padded_namespaces.txt"

OOV = "@@UNKNOWN@@"
PAD = "@@PADDING@@"

def read_lines_clean(path: Path):
    """
    Read text as UTF-8 (handles BOM), normalize newlines, strip trailing \r/\n,
    and drop empty lines.
    """
    raw = path.read_bytes()
    # Handle UTF-8 BOM if present
    text = raw.decode("utf-8-sig", errors="replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.strip() for ln in text.split("\n")]
    lines = [ln for ln in lines if ln != ""]
    return lines

def write_lines_lf(path: Path, lines):
    """
    Write UTF-8 without BOM, LF newlines.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(lines) + "\n"
    path.write_bytes(content.encode("utf-8"))

def backup_file(path: Path, backup_dir: Path):
    if path.exists():
        shutil.copy2(path, backup_dir / path.name)

def fix_d_tags():
    # For your working inference/training, we keep this order:
    # CORRECT, INCORRECT, then PAD/OOV at the end.
    lines = ["CORRECT", "INCORRECT", OOV, PAD]
    write_lines_lf(DTAGS, lines)

def fix_labels():
    """
    Keep your existing label set, but normalize it and ensure:
    index 0: @@PADDING@@
    index 1: @@UNKNOWN@@
    """
    if not LABELS.exists():
        raise FileNotFoundError(f"Missing {LABELS}")

    lines = read_lines_clean(LABELS)

    # Remove any duplicates while preserving order
    seen = set()
    deduped = []
    for ln in lines:
        if ln not in seen:
            seen.add(ln)
            deduped.append(ln)

    # Remove PAD/OOV if they appear elsewhere; we will reinsert at top
    deduped = [ln for ln in deduped if ln not in (OOV, PAD)]

    # Put PAD/OOV first
    fixed = deduped + [OOV, PAD]

    # Basic sanity: labels should contain $KEEP and $DELETE somewhere
    if "$KEEP" not in fixed or "$DELETE" not in fixed:
        print("WARNING: labels.txt does not contain $KEEP/$DELETE after cleaning. "
              "This is unusual and may indicate the wrong vocab folder.")

    write_lines_lf(LABELS, fixed)

def fix_non_padded_namespaces():
    # This matches what we stabilized earlier:
    # - *labels means labels namespace is treated as non-padded (AllenNLP style)
    # - d_tags is explicitly non-padded so its indices don't get shifted unexpectedly
    lines = ["*tags", "*labels"]
    write_lines_lf(NON_PADDED, lines)

def main():
    if not VOCAB_DIR.exists():
        raise FileNotFoundError(f"Vocab dir not found: {VOCAB_DIR}")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    # Backup originals
    backup_file(DTAGS, BACKUP_DIR)
    backup_file(LABELS, BACKUP_DIR)
    backup_file(NON_PADDED, BACKUP_DIR)

    # Apply fixes
    fix_d_tags()
    fix_labels()
    fix_non_padded_namespaces()

    print("DONE.")
    print(f"Backups saved to: {BACKUP_DIR}")
    print(f"Wrote: {DTAGS}")
    print(f"Wrote: {LABELS}")
    print(f"Wrote: {NON_PADDED}")

if __name__ == "__main__":
    main()
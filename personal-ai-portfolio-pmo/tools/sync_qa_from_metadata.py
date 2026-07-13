import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "docs" / "qa-metadata-v2.md"
DATA = ROOT / "assets" / "qa-data.json"


def split_row(line):
    raw = line.strip().strip("|")
    cells = []
    current = []
    escaped = False
    for char in raw:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    cells.append("".join(current).strip())
    return cells


def split_terms(value):
    value = str(value or "").replace("<br>", "、")
    parts = re.split(r"[、,，;；]+", value)
    result = []
    seen = set()
    for part in parts:
        text = part.strip()
        key = re.sub(r"\s+", "", text).lower()
        if text and key not in seen:
            seen.add(key)
            result.append(text)
    return result


def read_metadata():
    rows = {}
    for line in META.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        if line.startswith("| ID") or line.startswith("|---"):
            continue
        cells = split_row(line)
        if len(cells) != 6 or not cells[0].isdigit():
            continue
        rows[int(cells[0])] = {
            "question": cells[1],
            "variants": split_terms(cells[2]),
            "keywords": split_terms(cells[3]),
            "module": cells[4],
            "recommended": cells[5] == "是",
        }
    return rows


def main():
    metadata = read_metadata()
    data = json.loads(DATA.read_text(encoding="utf-8"))

    synced = []
    for item in data:
        row = metadata.get(item["id"])
        if not row:
            continue
        item.update(row)
        item.pop("button", None)
        synced.append(item)

    source_ids = {item["id"] for item in data}
    removed = sorted(source_ids - set(metadata))
    extra = sorted(set(metadata) - source_ids)

    DATA.write_text(json.dumps(synced, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"metadata_rows={len(metadata)}")
    print(f"qa_items={len(synced)}")
    print(f"removed_from_qa={removed}")
    print(f"extra_in_metadata={extra}")
    print(f"wrote {DATA}")


if __name__ == "__main__":
    main()

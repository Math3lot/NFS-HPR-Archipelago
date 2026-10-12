"""
Reader for Need for Speed Hot Pursuit Remastered save files (*.NFS11Save).

The save is a small paged database:
- 0x180: 31 table blocks of 0x250 bytes. Each block holds the table name,
  the record size (u16 at +0x14), field definitions from +0x18 (16 bytes each:
  name[13], type u8, offset u16), and at +0x188 a page descriptor whose second
  u32 is the address of the table's first data page.
- Data pages: header of 0x1c bytes (magic 0xC00BACCA at +0, back-pointer to the
  table block at +0xC, used byte count u16 at +0x14), then packed records.
"""
from __future__ import annotations

import struct
import sys
from dataclasses import dataclass, field
from typing import Dict, List

TABLE_BASE = 0x180
TABLE_STRIDE = 0x250
TABLE_COUNT = 31
PAGE_MAGIC = 0xC00BACCA
PAGE_HEADER = 0x1C

# field type -> (struct format, size)
FIELD_TYPES = {
    0: ("<I", 4),   # u32 (ids)
    1: ("<f", 4),   # float
    3: ("<B", 1),   # u8
    4: ("<Q", 8),   # u64
    5: ("<B", 1),   # bool
    6: ("<B", 1),   # u8
    7: ("<H", 2),   # u16
    8: ("<I", 4),   # u32 (counters)
}


@dataclass
class Field:
    name: str
    type: int
    offset: int


@dataclass
class Table:
    index: int
    name: str
    record_size: int
    fields: List[Field]
    first_page: int
    rows: List[Dict[str, object]] = field(default_factory=list)


def _cstr(raw: bytes) -> str:
    return raw.split(b"\x00")[0].decode("ascii", errors="replace")


def parse(data: bytes) -> Dict[str, Table]:
    tables: Dict[str, Table] = {}
    for k in range(TABLE_COUNT):
        base = TABLE_BASE + k * TABLE_STRIDE
        name = _cstr(data[base + 4:base + 20])
        record_size = struct.unpack_from("<H", data, base + 0x14)[0]
        fields: List[Field] = []
        pos = base + 0x18
        while pos < base + 0x188:
            fname = _cstr(data[pos:pos + 13])
            if not fname or not fname[0].isalpha():
                break
            ftype = data[pos + 13]
            foffset = struct.unpack_from("<H", data, pos + 14)[0]
            fields.append(Field(fname, ftype, foffset))
            pos += 16
        first_page = struct.unpack_from("<I", data, base + 0x18C)[0]
        table = Table(k, name, record_size, fields, first_page)

        page = first_page
        seen = set()
        while page and page not in seen and page + PAGE_HEADER < len(data):
            seen.add(page)
            used = struct.unpack_from("<H", data, page + 0x14)[0]
            body = data[page + PAGE_HEADER:page + PAGE_HEADER + used]
            for r in range(0, used - used % record_size if record_size else 0, record_size):
                rec = body[r:r + record_size]
                row: Dict[str, object] = {}
                for f in fields:
                    fmt, size = FIELD_TYPES.get(f.type, ("<I", 4))
                    if f.offset + size <= len(rec):
                        row[f.name] = struct.unpack_from(fmt, rec, f.offset)[0]
                table.rows.append(row)
            nxt = struct.unpack_from("<I", data, page + 4)[0]
            page = nxt if nxt != page else 0
        tables[name] = table
    return tables


STAT_RACER_BOUNTY = 0x52434254  # 'RCBT' racer career bounty
STAT_COP_BOUNTY = 0x43504254    # 'CPBT' cop career bounty


def read_save(path: str) -> Dict[str, Table]:
    with open(path, "rb") as f:
        return parse(f.read())


def stat(tables: Dict[str, Table], stat_id: int) -> int:
    for row in tables["stat_i"].rows:
        if row.get("id") == stat_id:
            return int(row.get("value", 0))
    return 0

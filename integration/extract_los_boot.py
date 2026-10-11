"""Extract and verify boot from a full LOS update payload (stdlib only)."""
import bz2, hashlib, lzma, struct, sys, zipfile
from pathlib import Path

def varint(data, pos):
    n = shift = 0
    while True:
        b = data[pos]; pos += 1
        n |= (b & 127) << shift
        if not b & 128: return n, pos
        shift += 7
        if shift > 70: raise ValueError('invalid varint')

def fields(data):
    result = {}; pos = 0
    while pos < len(data):
        key, pos = varint(data, pos); wire = key & 7
        if wire == 0: value, pos = varint(data, pos)
        elif wire == 2:
            length, pos = varint(data, pos)
            value = data[pos:pos+length]; pos += length
        elif wire in (1, 5):
            length = 8 if wire == 1 else 4
            value = data[pos:pos+length]; pos += length
        else: raise ValueError('unsupported protobuf wire type')
        result.setdefault(key >> 3, []).append(value)
    return result

def one(f, key, default=None): return f.get(key, [default])[0]

with zipfile.ZipFile(sys.argv[1]) as archive, archive.open('payload.bin') as payload:
    header = payload.read(24)
    magic, version, length, signature_length = struct.unpack('>4sQQI', header)
    if magic != b'CrAU' or version != 2: raise ValueError('expected payload v2')
    manifest = fields(payload.read(length)); data_start = 24 + length + signature_length
    block_size = one(manifest, 3, 4096)
    partitions = [fields(p) for p in manifest[13]]
    part = next(p for p in partitions if one(p, 1) == (sys.argv[3].encode() if len(sys.argv) > 3 else b'boot'))
    info = fields(one(part, 7)); size = one(info, 1); expected = one(info, 2)
    output = Path(sys.argv[2])
    if output.exists(): raise FileExistsError(output)
    with output.open('xb+') as target:
        target.truncate(size)
        for raw in part[8]:
            op = fields(raw); kind = one(op, 1)
            if kind in (0, 1, 8):
                payload.seek(data_start + one(op, 2, 0))
                data = payload.read(one(op, 3, 0))
                digest = one(op, 8)
                if digest and hashlib.sha256(data).digest() != digest: raise ValueError('operation digest mismatch')
                if kind == 1: data = bz2.decompress(data)
                elif kind == 8: data = lzma.decompress(data)
            elif kind == 6: data = None
            else: raise ValueError('not a supported full-payload operation: %s' % kind)
            cursor = 0
            for raw_extent in op[6]:
                extent = fields(raw_extent); start = one(extent, 1); count = one(extent, 2) * block_size
                if start * block_size + count > size: raise ValueError('extent exceeds partition')
                target.seek(start * block_size)
                chunk = bytes(count) if data is None else data[cursor:cursor+count]
                if len(chunk) != count: raise ValueError('short operation')
                target.write(chunk); cursor += count
            if data is not None and cursor != len(data): raise ValueError('unused operation data')
        target.seek(0); actual = hashlib.sha256(target.read()).digest()
        if actual != expected: raise ValueError('partition digest mismatch')
    print('%s sha256=%s' % (output, actual.hex()))

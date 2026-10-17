"""Normalize an unused v2 recovery_dtbo offset for strict Android boot parsers.
When recovery_dtbo_size is zero, this changes no component location or contents.
"""
import argparse, json, struct
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
data=bytearray(a.input.read_bytes());assert data[:8]==b'ANDROID!';assert struct.unpack_from('<I',data,40)[0]==2
page=struct.unpack_from('<I',data,36)[0];assert page and page&(page-1)==0
size=struct.unpack_from('<I',data,1632)[0];assert size==0,'Only normalize an absent recovery_dtbo'
old=struct.unpack_from('<Q',data,1636)[0]
offset=page+sum((struct.unpack_from('<I',data,p)[0]+page-1)//page*page for p in (8,16,24))
assert old in (0,offset)
struct.pack_into('<Q',data,1636,offset)
assert data[:1636]==a.input.read_bytes()[:1636] and data[1644:]==a.input.read_bytes()[1644:]
with a.output.open('xb') as f:f.write(data)
print(json.dumps({'old_recovery_dtbo_offset':old,'new_recovery_dtbo_offset':offset,'recovery_dtbo_size':size,'component_bytes_unchanged':True}))

"""Minimal, strict reader/writer for the native @@b@ typed asset container.

Format confirmed against local EU5 1.3.11 files and the public io_pdx_mesh
format description: https://github.com/ross-g/io_pdx_mesh/blob/master/pdx_data.py
"""
import struct
from pathlib import Path

def node(name, props=None, children=None):
    return {'name':name,'props':props or {},'children':children or []}

def read(path):
    data=Path(path).read_bytes();assert data[:4]==b'@@b@'
    root=node('root');stack=[root];pos=4
    while pos<len(data):
        if data[pos]==91:
            depth=0
            while data[pos]==91:depth+=1;pos+=1
            end=data.index(0,pos);name=data[pos:end].decode('latin1');pos=end+1
            assert depth<=len(stack)
            stack=stack[:depth];child=node(name);stack[-1]['children'].append(child);stack.append(child)
        else:
            assert data[pos]==33,(path,pos)
            length=data[pos+1];pos+=2;name=data[pos:pos+length].decode('latin1');pos+=length
            typ=chr(data[pos]);count=struct.unpack_from('<I',data,pos+1)[0];pos+=5
            if typ=='s':
                assert count==1
                length=struct.unpack_from('<I',data,pos)[0];pos+=4
                value=data[pos:pos+length].rstrip(b'\0').decode('latin1');pos+=length
            else:
                assert typ in ('f','i')
                value=list(struct.unpack_from('<'+str(count)+typ,data,pos));pos+=count*4
            stack[-1]['props'][name]=(typ,value)
    assert pos==len(data)
    return root

def write(path,root):
    data=bytearray(b'@@b@')
    def emit(n,depth):
        if depth:data.extend(b'['*depth+n['name'].encode('latin1')+b'\0')
        for name,(typ,value) in n['props'].items():
            key=name.encode('latin1');assert len(key)<128
            data.extend(b'!'+bytes([len(key)])+key+typ.encode())
            if typ=='s':
                raw=value.encode('latin1')+b'\0';data.extend(struct.pack('<II',1,len(raw))+raw)
            else:
                data.extend(struct.pack('<I',len(value))+struct.pack('<'+str(len(value))+typ,*value))
        for child in n['children']:emit(child,depth+1)
    emit(root,0);Path(path).write_bytes(data)

def summary(n):
    return {'name':n['name'],'props':{k:(t,v if t=='s' or len(v)<=16 else f'{len(v)} values') for k,(t,v) in n['props'].items()},'children':[summary(c) for c in n['children']]}

if __name__=='__main__':
    import json,sys
    print(json.dumps(summary(read(sys.argv[1])),indent=2))

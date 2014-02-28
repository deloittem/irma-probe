#!/usr/bin/env python

import leveldb
import sys
from csv import DictReader
from binascii import unhexlify,hexlify

if len(sys.argv) != 2:
    print "Usage %s <nsrl_csvfile>"%sys.argv[0]
    sys.exit(1)


class Commiter(object):
    maxops = 1000

    def __init__(self,dbfile):
        self._nbop = 0
        self._db = leveldb.LevelDB(dbfile)
        self._batch = leveldb.WriteBatch()
        return
    
    def add(self, key,value,force_write):
        self._batch.Put(key,str(value))
        self._nbop += 1
        if self._nbop == self.maxops or force_write:
            self._db.Write(self._batch,sync=True)
            self._batch = leveldb.WriteBatch()
            self._nbop = 0
        return
        

with open(sys.argv[1],"r") as f:
    reader = DictReader(f)
    current_value = []
    key = None
    commiter = Commiter("./nsrldb")
    count = 0    
    for row in reader:
	if count%50000 == 0:
		print count
	count +=1
        current_key = unhexlify(row["SHA-1"])
        if not key: key = current_key
        if key != current_key:
            commiter.add(key,current_value,False)
            current_value = []
        current_value.append("%s,%s,%s,%s,%s"%(row["FileName"],row["FileSize"],row["ProductCode"],row["OpSystemCode"],row["SpecialCode"]))
        key = current_key
    if len(current_value) != 0:
        commiter.add(key,current_value,True)
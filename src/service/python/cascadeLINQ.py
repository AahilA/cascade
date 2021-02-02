#!/usr/bin/env python3
import cascade_py

class CascadeShardLinq:
    def __init__(self, capi, subgroup_index, shard_index, version=-2, ts=-1 _type):
        self.capi = capi
        self.subgroup_index = subgroup_index
        self.shard_index = shard_index
        self.version = version
        self.ts = ts
        self.type = _type

    def __iter__(self):

        if self.version != -2:
            store = self.capi.get_keylist(self.type, self.version, self.subgroup_index, self.shard_index)
            self.key_list = self.capi.get_result()
        else:
            store = self.capi.get_keylist_by_time(self.type, self.ts, self.subgroup_index, self.shard_index)
            self.key_list = self.capi.get_result()
        return self

    def __next__(self):
        if len(self.key_list) != 0:
            store = self.capi.get(self.type, self.key_list.pop(0), self.version, self.subgroup_index, self.shard_index)
            value = store.get_result()
            return value
        else:
            raise StopIteration
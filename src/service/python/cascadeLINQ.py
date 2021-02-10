#!/usr/bin/env python3
import cascade_py

class CascadeShardLinq:
    def __init__(self, capi, _type, subgroup_index, shard_index, version):
        self.capi = capi
        self.subgroup_index = subgroup_index
        self.shard_index = shard_index
        self.version = version
        self.type = _type
        self.gi_running = True

    def __iter__(self):

        store = self.capi.get_keylist(self.type, self.version, self.subgroup_index, self.shard_index)
        self.key_list = store.get_result()
        return self

    def __next__(self):
        if len(self.key_list) != 0:
            store = self.capi.get(self.type, str(self.key_list.pop(0)), self.version, self.subgroup_index, self.shard_index)
            value = store.get_result().bytes()
            return value.decode('utf-8')
        else:
            raise StopIteration

class CascadeShardLinqTime:
    def __init__(self, capi, _type, subgroup_index, shard_index, ts):
        self.capi = capi
        self.subgroup_index = subgroup_index
        self.shard_index = shard_index
        self.ts = ts
        self.type = _type
        self.gi_running = True

    def __iter__(self):
    
        store = self.capi.get_keylist_by_time(self.type, self.ts, self.subgroup_index, self.shard_index)
        self.key_list = store.get_result()
        return self

    def __next__(self):
        if len(self.key_list) != 0:
            store = self.capi.get(self.type, str(self.key_list.pop(0)), self.version, self.subgroup_index, self.shard_index)
            value = store.get_result().bytes()
            return value.decode('utf-8')
        else:
            raise StopIteration

class CascadeShardLinqVersion:
    def __init__(self, capi, _type, subgroup_index, shard_index, key, version):
        self.capi = capi
        self.subgroup_index = subgroup_index
        self.shard_index = shard_index
        self.version = version
        self.key = key
        self.type = _type
        self.over = False
        self.gi_running = True

    def __iter__(self):
        return self

    def __next__(self):
        if not self.over:
            store = self.capi.get(self.type, self.key, self.version, self.subgroup_index, self.shard_index)
            obj = store.get_result()
            version = obj.previous_version_by_key()
            value = obj.bytes()
            if version == 1:
                self.over = True
            return value.decode('utf-8')
        else:
            raise StopIteration

class CascadeShardLinqSubgroup:
    def __init__(self, capi, _type, subgroup_index, version):
        self.capi = capi
        self.subgroup_index = subgroup_index
        self.version = version
        self.shard_list = []
        self.type = _type
        self.ptr = 0
        self.gi_running = True

    def __iter__(self):
        
        noShards = self.capi.get_number_of_shards()
        for i in range(0,noShards):
            self.shard_list.append(CascadeShardLinq(self.capi, self.type, self.subgroup_index, i, self.version))
        return self

    def __next__(self):
        while self.ptr < len(self.shard_list):
            csl = self.shard_list[self.ptr]
            try:
                value = csl.__next__()
                return value.decode('utf-8')
            except:
                ptr+=1
        raise StopIteration
        
        


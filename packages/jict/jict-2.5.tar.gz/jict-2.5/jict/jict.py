#!/usr/bin/env python
from __future__ import print_function
from __future__ import division

from collections import defaultdict , deque
import sys, json, yaml, os, random, re ,copy, importlib, mmap
from bson.objectid import ObjectId
from time import time

from pymongo.collection import Collection as mgcoll
nolibs = []

try:
    import mysql.connector
except:
    nolibs.append( 'mysql-connector' )

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, deque):
            return list(o)

        try:
            return json.JSONEncoder.default(self, o)
        except:
            return str(o)

def sqlconnect(str):
    if 'mysql-connector' in nolibs:
        raise Exception('strore sql rquieres \'mysql-connector\' module')

    user,pawd,host,database = re.findall(
        "(.*):(.*)@([0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}):(.*)"
    , str )[0]
    cnt = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=pawd
    )
    return cnt

def loader(nd):
    nam, ext = os.path.splitext( nd )

    if not os.path.exists( nd ):
        file = open( nd, "w+" )
        file.write('{}')
        file.close()

    file = open( nd, "r+" )
    text = file.read()
    file.close()

    data = {}
    if text.strip() == '':
        return data
    elif ext == '.yaml':
        data = yaml.safe_load( text )
    elif ext == '.json':
        data = json.loads(text )
    elif text.strip() == '':
        data = {}

    return data

def to_jict(prev):
    nd = jict()
    for k,i in prev.items():
        if isinstance(i,dict):
            nd[k] = to_jict(i)

        # elif isinstance(i,list):
        #     nl = []
        #     for l in i:
        #         if isinstance(l,dict):
        #             nl.append(to_jict(l))
        #         else:
        #             nl.append(l)
        #     nd[k] = nl

        else:
            nd[k] = i
    return nd

class jict( defaultdict ):
    generator = None
    storepath = None

    def __new__(self, nd = None, extra = None):
        if isinstance( nd, dict ):
            dt = to_jict(nd)
            return dt

        elif isinstance( nd , mgcoll ):
            jct = jict()
            k = nd.find({'key':extra})
            if k.count() >= 1:
                jct = jict(next(k))

            jct.generator = nd
            jct.storepath = extra
            return jct
        elif isinstance( nd, str ):
            try:
                if len(nd) >= 5 and nd[-5:] in [ '.yaml' , '.json' ]:
                    if ( nd[:6] == 'shm//:' or nd[:6] == 'set://' ) and nd[-5:] == '.json':
                        nd = nd[6:]
                        dt = to_jict( loader(nd) )
                        dt.storepath = nd

                        f = open( nd, "r+b" )
                        dt.file = mmap.mmap( f.fileno() , 0 )
                        return dt

                    if not os.path.exists( nd ):
                        open( nd , 'w+' ).close()

                    dt = to_jict( loader(nd) )
                    dt.storepath = nd
                elif nd[-4:] == '.env' or '.env.example' in nd:
                    file = open( nd, "r+" )
                    text = file.read()
                    file.close()
                    jct = jict()
                    for x in text.split('\n'):
                        if x == '': continue
                        if '=' in x:
                            fields = x.split('=')
                            if len(fields) == 2:
                                k,v = fields
                                jct[k] = v

                    jct.storepath = nd
                    return jct
                else:
                    dt = to_jict( json.loads( nd ) )
            except Exception as e:
                dt = jict()

            return dt

        return super(jict, self).__new__(self, nd )

    def __init__(self, nd = None , extra = ''):
        self.factory = jict
        defaultdict.__init__( self, self.factory )

    # def __iter__(self):
    #     started = False
    #
    #     if self.generator != None:
    #         if not started:
    #             started = True
    #             yield jict(self.dict())
    #
    #         for x in self.generator:
    #             yield to_jict(x)

    def has(self, args ):
        keys= self.keys()
        for x in args:
            if x not in keys: return False
        return True

    # creates a default valuef for the key if doesn't has on
    def init(self,key, deft ):
        if key in self.keys():
            return self[key]

        self[key] = deft
        return self[key]

    def __iadd__(self, other):
        typ = type(other)

        if typ == int:
            return 0 + other

        if typ == dict:
            other = jict(other)
            typ = jict

        if typ == jict:
            for x in other.keys():
                if x not in self.keys():
                    self[x] = other[x]
                else:
                    self[x] += other[x]

        return self

    def set_max(self,key,val,create = False):
        if key not in self.keys():
            if not create: return self[key]
            else:
                self[key] = val
                return self[key]

        if self[key] == None:
            self[key] = 0

        self[key] = val if val > self[key] else self[key]
        return self[key]

    def set_min(self,key,val,create = False ):
        if key not in self.keys():
            if not create: return self[key]
            else:
                self[key] = val
                return self[key]

        if self[key] == None:
            self[key] = 10 ** 15

        self[key] = val if val < self[key] else self[key]
        return self[key]

    def drop(self ,target = None):

        def ittrlis(val,tar):
            for l in val:
                if isinstance(l,jict):
                    l.drop(tar)
                if isinstance(l,list):
                    ittrlis(l,tar)

        for x in self.keys():
            val = self[x]
            if isinstance(val , jict):
                val.drop( target )

            if isinstance(val , list ):
                ittrlis(val, target)

            if val == target:
                del self[x]

    def rename(self,target,replace):
        def ittrlist(lst,tg,rp):
            nl = []
            for x in lst:
                if isinstance(x,jict):
                    x.rename(tg,rp)
                if isinstance(x,dict):
                    jct = jict(x)
                    jct.rename(tg,rp)
                    x = jct.dict()
                if isinstance(x,list):
                    x = ittrlist(x,tg,rp)

                nl.append(x)
            return nl

        for k in self.keys():
            val = self[k]
            if isinstance(val,list):
                self[k] = ittrlist(val,target,replace)
            if isinstance(val,jict):
                val.rename(target,replace)
            if isinstance(val,dict):
                jct = jict(val)
                jct.rename(target,replace)
                self[k] = jct.dict()
            if k == target:
                self[replace] = self.pop(target)

    def replace(self, target , replacef = None ):

        if replacef == None and isinstance(target,dict):
            for k in target.keys():
                self.replace(k,target[k])
            return

        def ittrlist(lst,tg,rp):
            nl = []
            for x in lst:
                if isinstance(x,jict):
                    x.replace(tg,rp)
                if isinstance(x,dict):
                    jct = jict(x)
                    jct.replace(tg,rp)
                    x = jct.dict()
                if isinstance(x,list):
                    x = ittrlist(x,tg,rp)
                nl.append(x)
            return nl

        for k in self.keys():
            val = self[k]
            if isinstance(val,list):
                self[k] = ittrlist(val,target,replacef)
            if isinstance(val,jict):
                val.replace(target,replacef)
            if isinstance(val,dict):
                jct = jict(val)
                jct.replace(target,replacef)
                self[k] = jct.dict()

            if k == target:
                if hasattr(replacef, '__call__'):
                    self[k] = replacef(val)
                else:
                    self[k] = replacef

    def _ittrlist(self,lst,k,luky=True ):
        found = []
        for x in lst:
            if isinstance(x,list):
                found += self._ittrlist(x,k,luky)
                continue
            elif isinstance(x,dict) or isinstance(x,jict):
                found += self._ittrdict(x,k,luky)
        return found

    def _ittrdict(self,dic,k ,luky = True ):
        found = []
        for x in dic.keys():
            val = dic[x]

            if x == k:
                found.append(val)
                if luky: return found
                continue

            if isinstance(val, list):
                found += self._ittrlist(val,k,luky)
                continue

            elif isinstance(val,dict) or isinstance(val,jict):
                found += self._ittrdict(val,k,luky)

        return found

    def get(self,key,luky = True ):
        ret = self._ittrdict(self,key, luky )

        if len(ret) == 1:
            return ret[-1]
        elif len(ret) > 1:
            return ret

        return None

    def dict(self, input_dict=None ):
        plain_dict = dict()
        if input_dict is None:
            input_dict = self
        for key in input_dict.keys():
            value = input_dict[key]
            if isinstance(value, jict):
                plain_dict[ key ] = self.dict(value)
            else:
                plain_dict[ key ] = value
        return plain_dict

    def random(self):
        for x in range( random.randint(0, 9) ):
            self[x] = x
            if random.randint(0, 1) == 0:
                self[x] = [ f for f in range(random.randint(0, 10)) ]

    def __str__(self):
        return self.json()

    def json(self,indent=2):
        if indent == 0: return json.dumps( self.dict() , cls= JSONEncoder )
        return json.dumps( self.dict() , indent = indent , cls= JSONEncoder )

    def yaml(self):
        return yaml.dump(yaml.full_load( self.json(0) ), default_flow_style=False)

    def __getitem__(self,key):
        jct = super( defaultdict, self ).__getitem__(key)

        if hasattr( self , 'skig' ):
            return jct

        if hasattr( self , 'file' ):
            mm = self.file
            mm.seek( 0 )
            text = mm.read(mm.size())
            data = json.loads( text )
            dt = jict( data )
            val = dt[key]

            setattr(self,'skip',True)
            self[key] = val
            del self.skip
            return val

        return jct

    def __setitem__( self , key , data ):
        super(defaultdict, self).__setitem__( key , data )

        # stops the infinite set
        if hasattr( self , 'skip' ):
            return

        if hasattr( self , 'file' ):
            mm = self.file

            setattr(self,'skig',True)
            ns = bytes( self.json( 0 ) , 'utf-8')
            del self.skig
            mm.seek( 0 )
            if mm.size() != len( ns ):
                mm.resize( len( ns ) )

            mm.seek( 0 )
            mm.write(ns)

    def deque(self,key,data,maxlen = 5 ):
        if not isinstance(self[key], deque ):
            if isinstance(self[key], list ):
                self[key] = deque(self[key], maxlen = maxlen)
            else:
                self[key] = deque(maxlen = maxlen)

        self[key].append( data )
        if hasattr( self , 'file' ):
            mm = self.file

            setattr(self,'skig',True)
            ns = bytes( self.json( 0 ) , 'utf-8')
            del self.skig

            mm.seek( 0 )
            if mm.size() != len( ns ):
                mm.resize( len( ns ) )

            mm.seek( 0 )
            mm.write(ns)

    def close(self):
        if hasattr( self , 'file' ):
            self.file.flush()
            self.file.close()

    def save(self, name = None, tp = None , shm = '' ):
        if hasattr( self , 'file' ):
            return

        if isinstance(self.generator, mgcoll ):
            if '_id' not in self.keys():
                k = self.generator.find({'key':self.storepath})
                if k.count() >= 1:
                    self['_id'] = next(k)['_id']

            if '_id' not in self.keys():
                self.generator.insert_one({ 'data':self.dict(), 'key': self.storepath })
            else:
                self.generator.update_one(
                    { '_id':self['_id'] },{ '$set':{'data':self.dict()} }
                )

            return
        # if name != None:
        #     valid = ['sql://']
        #
        #     for x in valid:
        #         if len(name) >= len(x) and name[:len(x)] == x:
        #             if name[:len(x)] == 'sql://':
        #                 self.sql_store(name[len(x):])
        #                 return

        self.storepath = name if name != None else self.storepath \
                    if self.storepath != None else 'jict.json'

        nam, ext = os.path.splitext( self.storepath )
        tp = ext if tp == None else '.' + tp if not tp[0] == '.' else tp
        self.storepath = nam + tp

        f = open(self.storepath, "w+")
        if tp == '.example' or self.storepath[-4:] == '.env':
            txt = ''
            for x in self.keys():
                if isinstance( self[x] ,str ):
                    txt += f'{x}={self[x]}\n'
            f.write( txt )
        elif tp == '.yaml':
            f.write( self.yaml() )
        else:
            f.write( self.json() )

        f.close()

    # def sql_store(self,db):
    #     connection = sqlconnect()
    #
    #     skip = ['columns']
    #
    #     for table in self.keys():
    #         lines = self[table]
    #
    #         if table in skip:
    #             continue
    #
    #         for line in lines:
    #             print( line )
    #
    #     cursor.close()
    #     connection.close()
    #
    #     del cursor
    #     del connection

## jict
jict is basically a nested dict.  
with some extra features  

simple use example :

```python
from jict import jict

jct = jict()
jct['level1']['level2']['level3'] = 'created nested dictionary'

print(jct)
# output :
# {
#   "level1": {
#     "level2": {
#       "level3": "created nested dictionary"
#     }
#   }
# }

# jict to dict
mydict = jct.dict()

```

jict utilities:
```python
from jict import jict

# our jict
jct = jict({
    'val': { 'list':[ [{ 'find-me': 'secret' }] ] }
})

# we can easly find the key we need
print(jct.get('find-me'))

# we also can rename the keys
# output : secret
jct.rename('find-me','password')
print(jct.get('find-me'))
# output : None
print(jct.get('password'))
# output : secret

# we also can replace values
jct.replace('password','mypass')
print(jct.get('password'))
# output : mypass


def foo(val):
    val[0][0]['name'] = 'jict'
    return val

# we also can replace with callbacks and multiple values
jct.replace({
    'password':'mypass',
    'list': foo,
})

# callbacks also work with this: jct.replace('list' , foo)

print(jct.get('list'))
# output: [[{'password': 'mypass', 'name': 'jict'}]]


```

also you can easly load a .json , .yaml file

```python
from jict import jict

jctj = jict('test.json')
print(jctj)
# output :
# {
#   "test": "json-content"
# }

jcty = jict('test.yaml')
print(jctj)
# output :
# {
#   "test": "yaml-content"
# }

# if you want to save the modifed values
jctj.save()
jcty.save()

# you can also save to another file
jcty.save('newfile.json')
```

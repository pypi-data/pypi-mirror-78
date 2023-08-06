# git-name

a git extension and python package for turning hashes into memorable names

# install

from pypi

`pip install git-name`

or from github master

`pip install git+https://github.com/CircArgs/git-name.git`

# Usage

## shell

```shell
CircArgs $ git name -h
usage: git name [-h] [-f] [-l LENGTH] word_or_hash

convert hashes to memorable names

positional arguments:
  word_or_hash

optional arguments:
  -h, --help            show this help message and exit
  -f, --from            `from hash` flag used to denote argument is a hash.
  -l LENGTH, --length LENGTH
                        `hash length` (default=7) truncate the input output hash to this length

CircArgs $ git name efa8f31
ten occupied nuts

CircArgs $ git name -f "ten occupied nuts"
efa8f31

CircArgs $ git name -f "five fat frogs"
a42cd68

# use names with git instead of hashes
CircArgs $ git checkout $(git name -f "five fat frogs")
```

## python

```python
from git_name import NameGenerator

num=142152565

ng=NameGenerator()

name=ng.generate_name(num)

print(name)
# 'eight upward buttons'

name_num=ng.generate_num(name)
print(name_num)
#142152565

print(num==name_num)
#True

print(ng.generate_hash_from_name(name, 7))
#8791375

print(ng.generate_name_from_hash(8791375, 7)
#'eight upward buttons'


```

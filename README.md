# `raho`: Simple symmetric encryption

[![Build Status](https://travis-ci.org/abhayagiri/raho.svg?branch=master)](https://travis-ci.org/abhayagiri/raho)
[![Code Coverage](https://codecov.io/gh/abhayagiri/raho/branch/master/graph/badge.svg)](https://codecov.io/gh/abhayagiri/raho)
[![Support Python Versions](https://img.shields.io/pypi/pyversions/raho.svg)](https://pypi.org/project/raho/)
[![Latest Version](https://img.shields.io/pypi/v/raho.svg)](https://pypi.org/project/raho/)

`raho` is a simplified wrapper library for the
[cryptography](https://cryptography.io/) module.

## Installation

```sh
pip install raho
```

And in your Python file:

```python
>>> import raho

```

## Usage

### With Fernets

```python
>>> fernet = raho.generate_fernet()
>>> message = raho.encrypt('he is hiding behind the rock', fernet)
>>> message
'Z0FB...'
>>> raho.decrypt(message, fernet)
'he is hiding behind the rock'

```

### With passwords

```python
>>> message = raho.encrypt_with_password('they know water', 'dragon123')
>>> raho.decrypt_with_password(message, 'dragon123')
'they know water'

```

### With key files

```python
>>> fernet = raho.generate_key_file('key-file')
>>> message = raho.encrypt_with_key_file('falcon flies at dawn', 'key-file')
>>> raho.decrypt_with_key_file(message, 'key-file')
'falcon flies at dawn'

```

### Command line

See `raho --help` for command-line usage examples.

## More information

- [Fernets and `cryptography`](https://cryptography.io/)
- [Development Documentation](https://github.com/abhayagiri/raho/blob/master/DEVELOPMENT.md)

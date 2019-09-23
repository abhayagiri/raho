# `raho` Development

## Setup

Install [Python](https://www.python.org/), [tox](https://tox.readthedocs.io/),
[twine](https://twine.readthedocs.io/) and other dependencies:

```sh
sudo apt-get install -y curl git python3-dev python3-setuptools python3-wheel \
    tox twine
```

Install [pyenv](https://github.com/pyenv/pyenv-installer) (if not already
installed):

```sh
curl https://pyenv.run | bash
cat <<'EOF' >> "$HOME/.bashrc"
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
EOF
source "$HOME/.bashrc"
```

Clone the source tree:

```sh
git clone https://github.com/abhayagiri/raho.git
cd raho
```

Install the Python versions for testing with `pyenv`:

```sh
for v in $(cat .python-version); do
    [ "$v" != "system" ] && pyenv install -s $v
done
```

## Common Commands

### Test

```sh
tox
```

### Build

```sh
python3 setup.py sdist bdist_wheel --universal
```

### Upload to `test.pypi.org`

```sh
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

### Upload to `pypi.org`

```sh
twine upload dist/*
```

### Clean

```sh
rm -rf __pycache__ .coverage .tox build coverage.xml dist *.egg-info *.pyc
```

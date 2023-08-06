# xy-cli

[exiahuang/xy-cli](https://github.com/exiahuang/xy-cli) is a xy command tools.

# install

## install from pip

```sh
pip3 install xy-cli
```

## install from git

```sh
git clone https://github.com/exiahuang/xy-cli
python3 setup.py install
```

## green install

```sh
xy_cli=`pwd`
export PYTHONPATH="$xy_cli:$PYTHONPATH"
python3 -m xy_cli
```


# Usage

```
xy clone -f from_directory -t to_directory -d DATA1=NewData1 DATA2=NewData2 DATA3=NewData3
```


# package

```sh
python3 setup.py sdist
python3 setup.py bdist_wininst
```

## py2exe build windows exe

```sh
py -3.4 -m venv .py34
.py34\Scripts\activate.bat
# python -m pip install --upgrade pip
pip install py2exe setuptools
pip install requests XlsxWriter
python -V
python setup.py py2exe
```

# Acknowledgement

## Basic on OpenSource

# history

- 2020/08/30 init project
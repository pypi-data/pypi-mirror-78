# Package for common utils of avatar ecosystem

### Install to your service

```bash
pip install avatar-utils
```
That's all. Nothing more.

#
### Developers tips (how to upload a new version)

##### Install setuptools and wheel

```bash
pip install setuptools wheel
```

##### Generate distribution package

```bash
python setup.py sdist bdist_wheel
```

##### Install twine

```bash
pip install twine
```

##### Upload package to index

```bash
python -m twine upload dist/*
```

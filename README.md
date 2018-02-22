# 35_diff_service

Shows a difference betwen 2 text files

# How to install

Python 3 should be already installed. Then use pip (or pip3 if there is
a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.


# How to use

## In console

```python
python diff.py path/to/file_1 path/to/file_2> #  or python3
```

Result is text with differences

## As website

1. Run server:
```python
python app.py #  or python3
```
2. Browse [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## As api

1. Run server:
```python
python app.py #  or python3
```

2. Send request
```
POST http://127.0.0.1:5000/api/v1.0/diff
Content-Type: application/json
```

Params:
```json
{
    "doc1": "text1",
    "doc2": "text2",
    "config": {//any config param are not required
       "deleted_element": "del",
        "inserted_element": "ins",
        "modified_class": "diff modified",
        "deleted_class": "diff deleted",
        "inserted_class": "diff inserted",
    }
}
```

Response:
```json
{
    "result": "<del class=\"diff modifieddd\">test1</del><ins class=\"diff modifieddd\">test2</ins>"
}
```

More in api help http://127.0.0.1:5000/api/help

# How to test

```python
python tests.py #  or python3
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

# Call-Record

## About
Implementing an application that receives call detail records and calculates monthly bills for a given telephone number.

More information at: https://github.com/olist/start-at-olist-backend

## Requirements:
 - [Python] >= 3.8
 - [Pip]

## How to Install

If you don't have poetry, install it with pip
```
pip install poetry
```

The following command installs all project dependencies
```
poetry install
```

The following command activates the virtual environment
```
poetry shell
```

Verify that it is at the same level as the manage.py file and enter the following command to run the migrations
```
./manage.py migrate
```

Still at the manage.py file level, enter the following command to start the server
```
./manage.py runserver
```

In the URL for [call], insert the data to initiate a phone call.

In the URL for [billing], it is possible to make a post request on the server, with insert the data to initiate a phone call.


[Python]: <https://www.python.org/downloads/>
[Pip]: <https://pip.pypa.io/en/stable/installing/>
[call]: <http://localhost:8000/call-record>
[billing]: <http://localhost:8000/bill/>
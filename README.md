[![Python - 3.9](https://img.shields.io/badge/Python-3.9-blue)](https://www.python.org/downloads/release/python-390/ "Python 3.9")
[![Maintained - yes](https://img.shields.io/badge/Maintained-Yes-green)](https://github.com/0xbow-io/asp-admin-dashboard "The Repository is well Maintained.")
[![Django - 4.2.9](https://img.shields.io/badge/Django-4.2.9-blue)](https://www.djangoproject.com/download/ "Django 4.2.9")


# django-llamaindex-google-drive-template

TBD

## Getting Started

These instructions will get your copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites

You need to have Python 3.9 installed on your machine. You also need pip for installing the dependencies. It usually comes with Python.

### Installing

After cloning the repository and navigating into the directory, install the dependencies using pip:
A step by step series of examples that tell you how to get a development environment running

```
pip install -r requirements.txt
```

Then, install the pre-commit hooks:

```
pre-commit install
```

Finally, run the migrations:

```
python manage.py migrate
```

## Running the tests

```
python manage.py test
```


## Running the server

```
python manage.py runserver
```

Run Celery:

```bash
celery -A core worker -P gevent -c 1000 --loglevel=info
```

Run Celery Beats:

```bash
celery -A core beat --loglevel=info
```

## Deployment

Add additional notes about how to deploy this on a live system

-- TBD

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [PostgreSQL](https://www.postgresql.org/) - The database used

## Contributing

TBD
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

TBD
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Amir Mehr** - *Initial work* - [ammirsm](https://github.com/ammirsm)

See also the list of [contributors](https://github.com/ammirsm/llm-email-cleaner/contributors) who participated in this project.

## License

TBD
This project is licensed under the [LICENSE NAME] License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

TBD

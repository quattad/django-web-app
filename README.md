## Quote Buddy

Quote Buddy is a simple web application that allows you to generate quotes using the [Quotes on Design API](https://quotesondesign.com/api-v4-0/).

## Description
See the project [here](http://quote-buddy.herokuapp.com/).

### Installation

Install virtualenvwrapper or virtualenvwrapper-win for Windows.

```
$ pip install virtualenvwrapper-win
```

Create and activate virtual environment.

```
$ mkvirtualenv quote-buddy
$ workon quote-buddy
```

Clone remote repository into desired local directory and install requirements using pip.

```
$ git clone https://github.com/quattad/quote-buddy.git
$ pip install -r requirements.txt
```

Create SQLite3 database

```
$ python manage.py makemigrations
$ python manage.py migrate
```

Collect staticfiles to ensure that staticfiles are executed.

```
$ python manage.py collectstatic
```

Run the development server:
```
$ python manage.py runserver
```

## Running the tests

Tests were created using pytest.

Change directory into the project folder and run

```
pytest
```

Tests are mainly centered around view.py files for the various applications. They are categorized into Authentication, Response, Post Requests and Conditionals.

## Deployment

The current prototype for Quote Buddy has been deployed on [Heroku](http://quote-buddy.herokuapp.com/).

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **Jonathan Quah** - [Github](https://github.com/quattad) | [Personal Website](https://quattad.github.io)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Big thanks to [Corey Schafer](https://github.com/CoreyMSchafer). This project (and my preliminary understanding of Django) was based on his tutorials.
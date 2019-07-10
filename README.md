# Django Web Application

This is a sample project done by following the tutorials of Corey Schafer to practice developing and deploying
a web application.

### Table of Contents
* [Prerequisites](#prerequisites)

### Prerequisites

```
Give examples
```

### Installing

Install virtualenvwrapper or virtualenvwrapper-win for Windows.

```
$ pip install virtualenvwrapper-win
```

Change directory to project folder and create migrations file:

```
$ python manage.py makemigrations
```

Check that generated migrations file (e.g. 0001_initial.py) contains SQL code to create table:

```
$ python manage.py sqlmigrate blog 0001
```

Create table blog_post:

```
$ python manage.py migrate
```

Check that table has been successfully created:

```
$ python 
```

Run the development server:
```
$ python manage.py runserver
```

Run Python API to access and retrieve from database:

```
$ python manage.py shell
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
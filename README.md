# CICADA - CookIeCutter Automated DRF Angular
CICADA uses [Cookiecutter](https://github.com/audreyr/cookiecutter) and a custom script to automatically populate an
AngularJS frontend that connects to your Django REST backend. This template makes some assumptions about your
backend, namely that it is a Django DRF-based backend with JWT authentication. Such a template for a backend can
be easily created with the [cc-automated-drf-template](https://github.com/TAMU-CPT/cc-automated-drf-template).

*Full tutorial with cc-automated-drf-template and CICADA coming soon!*

## Features
- Webpack configured
- backend communication with [Restangular](https://github.com/mgonto/restangular)
- creates list and detail controllers for all models
- creates list and detail partials for all models
- built-in JWT-based login/logout
- uses [angular-gravatar](https://github.com/wallin/angular-gravatar) for user icons
- support for multiple apps in the backend

## Installation
Install Cookiecutter:
```console
$ pip install cookiecutter
```
Give names for your directory, project, and app when prompted by Cookiecutter.
```console
$ cookiecutter https://github.com/TAMU-CPT/CICADA.git
dir_name [frontend-test]:
description [Test frontend]:
author [TAMU-CPT]:
app_name [testApp]:
```
Run the script to populate template using the path to your backend app's `models.py`:
```console
$ python script.py path/to/models.py
```

To install requirements and run, type:
```console
$ make
```

That's it! By default, your server will be running on port 10000 and pointing at
port 8000 for the backend.

## Multiple app support
Some Django projects have multiple apps in addition to the base application.
If you want to similarly generate files on your frontend for another app,
all you have to do is run the script again using the path to that app's `models.py`.

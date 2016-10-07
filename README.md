# CICADA - CookIeCutter Automated DRF Angular
CICADA uses [Cookiecutter](https://github.com/audreyr/cookiecutter) and a custom script to automatically populate an
AngularJS frontend that connects to your Django REST backend. This template makes some assumptions about your
backend, namely that it is a Django DRF-based backend with JWT authentication. Such a template for a backend can
be easily created with the [cc-automated-drf-template](https://github.com/TAMU-CPT/cc-automated-drf-template).

## Features
- Webpack configured
- creates default controllers
- built-in JWT-based login/logout

## Installation
Install Cookiecutter:
```console
$ pip install cookiecutter
```
Give names for your directory, project, and app when prompted by Cookiecutter:
```console
$ cookiecutter https://github.com/TAMU-CPT/CICADA.git
dir_name [frontend-test]:
description [Test frontend]:
author [TAMU-CPT]:
app_name [testApp]:
models_path [~/Work/drf_project/base/models.py]:
```
Run the script:
```console
$ python script.py
```

Install requirements and run:
```console
$ npm install
$ make run
```

That's it! By default, your server will be running on port 10000 and pointing at
port 8000 for the backend. Don't forget to set up CORS in your backend.

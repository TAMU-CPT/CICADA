import os
import ast
import _ast

path = '{{cookiecutter.models_path}}'
models = []
app_name = '{{cookiecutter.app_name}}'

# parse models.py
with open(os.path.expanduser(path)) as models_file:
    m = ast.parse(models_file.read())
    for i in m.body:
        if type(i) == _ast.ClassDef:
            models.append(i.name)

with open('js/app.js', 'r+') as app:
    a = app.read()
    routes = []
    requires = []
    n = 0
    for num, model in enumerate(models):
        # first line will already be indented
        if num > 0:
            n = 12

        # list view
        routes.append('\n'.join([" "*n  + "when('/', {",
                   " "*16 + "templateUrl: 'partials/%s-list.html'," % model.lower(),
                   " "*16 + "controller: '%sListCtrl'" % model,
                   " "*12 + "})."]))

        # detail view
        routes.append('\n'.join([" "*12  + "when('/', {",
                   " "*16 + "templateUrl: 'partials/%s-detail.html'," % model.lower(),
                   " "*16 + "controller: '%sDetailCtrl'" % model,
                   " "*12 + "})."]))

        os.makedirs('./ctrl/%s' % model.lower())
        requires.append("require('./ctrl/%s/list.js')" % model.lower() + "(%s);" % app_name)
        requires.append("require('./ctrl/%s/detail.js')" % model.lower() + "(%s);" % app_name)

    a = a.replace('// LOAD ROUTES', '\n'.join(routes))
    a = a.replace('// REQUIRE', '\n'.join(requires))

    app.seek(0)
    app.truncate()
    app.write(a)

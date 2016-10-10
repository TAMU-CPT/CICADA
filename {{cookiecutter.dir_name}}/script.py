import os
import ast
import _ast

path = '{{cookiecutter.models_path}}'
app_name = '{{cookiecutter.app_name}}'
models = []

def template_ctrl(name):
    """ templates the contents of the controller files """
    return '\n'.join(["export default function(%s) {" % app_name,
                " "*4 + "%s" % app_name + ".controller('%s', ['$scope','$location'," % name,
                " "*8 + "function($scope, $location) {",
                " "*4 + "}]);",
                "}"])

# parse models.py
with open(os.path.expanduser(path)) as models_file:
    m = ast.parse(models_file.read())
    for i in m.body:
        if type(i) == _ast.ClassDef:
            models.append(i.name)

# modify app.js and create controllers and templates for list/detail views
with open('js/app.js', 'r+') as app:
    a = app.read()

    routes = []
    requires = []
    n = 0
    for num, model in enumerate(models):
        # first line will already be indented
        if num > 0:
            n = 12

        plural = 's'
        if model.endswith('s'):
            plural = 'es'

        # list view
        routes.append('\n'.join([" "*n  + "when('/%(0)s%(1)s', {" % {'0': model.lower(), '1': plural},
                   " "*16 + "templateUrl: 'partials/%s-list.html'," % model.lower(),
                   " "*16 + "controller: '%sListCtrl'" % model,
                   " "*12 + "})."]))

        # detail view
        routes.append('\n'.join([" "*12  + "when('/%(0)s%(1)s/:%(0)sID', {" % {'0': model.lower(), '1': plural},
                   " "*16 + "templateUrl: 'partials/%s-detail.html'," % model.lower(),
                   " "*16 + "controller: '%sDetailCtrl'" % model,
                   " "*12 + "})."]))

        requires.append("require('./ctrl/%s/list.js')" % model.lower() + "(%s);" % app_name)
        requires.append("require('./ctrl/%s/detail.js')" % model.lower() + "(%s);" % app_name)

        # create directories for each model's set of controls
        controller_path = 'js/ctrl/%s' % model.lower()
        os.makedirs(controller_path)

        # create list and detail controllers for each model
        with open(controller_path + '/list.js', 'w') as list_ctrl:
            list_ctrl.write(template_ctrl(model + "ListCtrl"))
        with open(controller_path + '/detail.js', 'w') as detail_ctrl:
            detail_ctrl.write(template_ctrl(model + "DetailCtrl"))

        # create list and detail templates for each model
        open('partials/%s-list.html' % model.lower(), 'a').close()
        open('partials/%s-detail.html' % model.lower(), 'a').close()

    a = a.replace('// LOAD ROUTES', '\n'.join(routes))
    a = a.replace('// REQUIRE', '\n'.join(requires))

    app.seek(0)
    app.truncate()
    app.write(a)

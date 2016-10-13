import os
import ast
import _ast

path = '{{cookiecutter.models_path}}'
app_name = '{{cookiecutter.app_name}}'
models = {}

def write_headers(model):
    return ('\n' + " "*28).join(["<th md-column><span>%s</span></th>" % field for field in models[model]])

def write_rows(model):
    return ('\n' + " "*28).join(["<td md-cell>{% raw %}{{%s.%s}}{% endraw %}</td>" % (model.lower(), field) for field in models[model]])

def template_ctrl(name):
    """ templates the contents of the controller files """
    return '\n'.join(["export default function(%s) {" % app_name,
                " "*4 + "%s" % app_name + ".controller('%s', ['$scope','$location','Restangular'," % name,
                " "*8 + "function($scope, $location, Restangular) {\n"])

# parse models.py
with open(os.path.expanduser(path)) as models_file:
    m = ast.parse(models_file.read())
    for i in m.body:
        if type(i) == _ast.ClassDef:
            models[i.name] = {}
            for x in i.body:
                if type(x) == _ast.Assign:
                    models[i.name][x.targets[0].id] = x.value.func.attr

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
            with open('list-template.js', 'r') as template:
                content = template.read()
                content = content.replace('&app&', os.path.basename(os.path.dirname(os.path.expanduser(path))))
                content = content.replace('&l&', model.lower())
                list_ctrl.write(content)
            list_ctrl.write('\n'.join([" "*4 + "}]);", "}"]))

        with open(controller_path + '/detail.js', 'w') as detail_ctrl:
            detail_ctrl.write(template_ctrl(model + "DetailCtrl"))
            detail_ctrl.write('\n'.join([" "*4 + "}]);", "}"]))

        # create list and detail templates for each model
        with open('list-template.html', 'r') as template:
            with open('partials/%s-list.html' % model.lower(), 'w') as partial:
                content = template.read()
                content = content.replace('&c&', model.lower())
                content = content.replace('&l&', model.lower())
                content = content.replace('&headers&', write_headers(model))
                content = content.replace('&rows&', write_rows(model))
                partial.write(content)

        # with open('detail-template.html', 'r') as template:
            # with open('partials/%s-detail.html' % model.lower(), 'w') as partial:
        # open('partials/%s-list.html' % model.lower(), 'a').close()
        # open('partials/%s-detail.html' % model.lower(), 'a').close()

    a = a.replace('// LOAD ROUTES', '\n'.join(routes))
    a = a.replace('// REQUIRE', '\n'.join(requires))

    app.seek(0)
    app.truncate()
    app.write(a)

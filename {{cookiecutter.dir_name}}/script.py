import os
import ast
import _ast
import argparse


def write_input_block(model,field):
    """ templates input blocks for card in detail view """
    return ('\n' + " "*16).join([" "*16 + '<md-input-container flex>',
                                 " "*4 + '<label>%s</label>' % field,
                                 " "*4 + '<input disabled ng-model="%s.%s">' % (model.lower(), field),
                                 '</md-input-container>'])

def write_inputs(model):
    """ returns templated input blocks for card in detail view """
    return ('\n').join(
        [write_input_block(model, field) \
         for field in models[model] \
         if models[model][field] != 'ManyToManyField'
        ])

def write_headers(model):
    """ templates headers for table in list view """
    return ('\n' + " "*28).join(
        ["<th md-column><span>%s</span></th>" % field \
         for field in models[model] \
         if models[model][field] != 'ManyToManyField'
        ])

def write_rows(model):
    """ templates rows for table in list view """
    return ('\n' + " "*28).join(
        ["<td md-cell>{% raw %}{{%s.%s}}{% endraw %}</td>" % (model.lower(), field) \
         for field in models[model] \
         if models[model][field] != 'ManyToManyField'
        ])

def template_ctrl(model, c_type, app_name, path, plural):
    """ templates the contents of the controller files """
    file_text = []
    controller_name = model + c_type + 'Ctrl'
    file_text.append('\n'.join(["export default function(%s) {" % app_name,
                               " "*4 + "%s" % app_name + ".controller('%s', ['$scope','$location','$routeParams', 'Restangular'," % controller_name,
                               " "*8 + "function($scope, $location, $routeParams, Restangular) {"]))

    with open('%s-template.js' % c_type.lower(), 'r') as template:
        content = template.read()
        content = content.replace('&app&', os.path.basename(os.path.dirname(os.path.expanduser(path))))
        content = content.replace('&l&', model.lower())
        content = content.replace('&plural&', plural)
        file_text.append(content)

    file_text.append('\n'.join([" "*4 + "}]);", "}"]))
    return '\n'.join(file_text)

def parse_models(path):
    """ parses models.py """
    models = {}
    with open(os.path.expanduser(path)) as models_file:
        m = ast.parse(models_file.read())
        for i in m.body:
            if type(i) == _ast.ClassDef:
                models[i.name] = {}
                for x in i.body:
                    if type(x) == _ast.Assign:
                        models[i.name][x.targets[0].id] = x.value.func.attr
    return models

# modify app.js and create controllers and templates for list/detail views
def write_files(models, path):
    with open('js/app.js', 'r+') as app:
        app_name = '{{cookiecutter.app_name}}'

        a = app.read()

        routes = []
        requires = []
        for model in models:
            plural = 's'
            if model.endswith('s'):
                plural = 'es'

            # list view
            routes.append('\n'.join([" "*12  + "when('/%(0)s%(1)s', {" % {'0': model.lower(), '1': plural},
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
                list_ctrl.write(template_ctrl(model, "List", app_name, path, plural))

            with open(controller_path + '/detail.js', 'w') as detail_ctrl:
                detail_ctrl.write(template_ctrl(model, "Detail", app_name, path, plural))

            # create list and detail templates for each model
            with open('list-template.html', 'r') as template:
                with open('partials/%s-list.html' % model.lower(), 'w') as partial:
                    content = template.read()
                    content = content.replace('&c&', model)
                    content = content.replace('&l&', model.lower())
                    content = content.replace('&plural&', plural)
                    content = content.replace('&headers&', write_headers(model))
                    content = content.replace('&rows&', write_rows(model))
                    partial.write(content)

            with open('detail-template.html', 'r') as template:
                with open('partials/%s-detail.html' % model.lower(), 'w') as partial:
                    content = template.read()
                    content = content.replace('&c&', model)
                    content = content.replace('&plural&', plural)
                    content = content.replace('&id&', '{% raw %}{{%s.id}}{% endraw %}' % model.lower())
                    content = content.replace('&inputs&', write_inputs(model))
                    partial.write(content)

        # keep flags in case there are multiple backend apps
        routes.append('// LOAD ROUTES')
        requires.append('// REQUIRE')
        a = a.replace('// LOAD ROUTES', '\n'.join(routes))
        a = a.replace('// REQUIRE', '\n'.join(requires))

        app.seek(0)
        app.truncate()
        app.write(a)

    # modify home.js to include links to all model list views
    with open('js/ctrl/home.js', 'r+') as home:
        h = home.read()
        homeitems = []
        for model in models:
            plural = 's'
            if model.endswith('s'):
                plural = 'es'
            homeitems.append(('\n' + " "*16).join([" "*16 + '{',
                                        " "*4 + 'title: "%s%s",' % (model, plural),
                                        " "*4 + 'url: "#/%s%s",' % (model.lower(), plural),
                                        '},']))

        homeitems.append('// LOAD HOMEITEMS')
        h = h.replace('// LOAD HOMEITEMS', '\n'.join(homeitems))
        home.seek(0)
        home.truncate()
        home.write(h)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='automatically populate an AngularJS frontend')
    parser.add_argument("models_path", help='path to models.py')
    args = parser.parse_args()

    models = parse_models(args.models_path)
    write_files(models, args.models_path)

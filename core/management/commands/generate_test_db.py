from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import core.settings as settings


init_apps_all = (
    "testing",
)

default_init = (
    (
        User.objects.filter(username="testparticipant").exists(),
        lambda: User.objects.create_user("testparticipant", password="testersGonnaTest")
    ),
    (
        User.objects.filter(username="testadmin").exists(),
        lambda: User.objects.create_user("testadmin", password="testersGonnaTest")
    )
)


class Command(BaseCommand):

    def run_from_argv(self, argv):
        for init_if, init_func in default_init:
            if init_if:
                init_func()

        initialised = set()
        init_apps = argv[2:]

        if len(argv[2:]) == 0:
            init_apps = init_apps_all

        for imp_path in init_apps:
            splitted_path = imp_path.split('.', maxsplit=2)
            if len(splitted_path) == 2:
                app, model_name = splitted_path
                if app in settings.INSTALLED_APPS:
                    app_models = apps.all_models[app]
                    # print(app_models)
                    if model_name.lower() in app_models:
                        model = app_models[model_name.lower()]

                        if getattr(app_models[model_name.lower()], 'get_test_instances', False):
                            if model not in initialised:
                                instances = model.get_test_instances()
                                if getattr(instances, '__iter__', False):
                                    for instance in instances:
                                        instance.evaluate()
                                        initialised = initialised.union(instance.evaluated_models)
                                else:
                                    instances.evaluate()
                                    initialised = initialised.union(instances.evaluated_models)
                            else:
                                print("Model %s already initialised" % model.__qualname__)
                        else:
                            print('WARNING: Model %s cant be initialised: missing get_test_instances method!'
                                  % model.__qualname__)
            elif len(splitted_path) == 1:
                app = splitted_path[0]
                if app in settings.INSTALLED_APPS:
                    app_models = apps.all_models[app]
                    for model_name, model in app_models.items():
                        if getattr(app_models[model_name.lower()], 'get_test_instances', False):
                            if model not in initialised:
                                instances = model.get_test_instances()
                                if getattr(instances, '__iter__', False):
                                    for instance in instances:
                                        instance.evaluate()
                                        initialised = initialised.union(instance.evaluated_models)
                                else:
                                    instances.evaluate()
                                    initialised = initialised.union(instances.evaluated_models)
                            else:
                                print("Model %s already initialised" % model.__qualname__)
                        else:
                            print('WARNING: Model %s cant be initialised: missing get_test_instances method!'
                                  % model.__qualname__)

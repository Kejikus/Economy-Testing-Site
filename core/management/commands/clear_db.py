from core.models import BaseModel
from core import settings
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def run_from_argv(self, argv):
        for imp_path in argv[2:]:
            splitted_path = imp_path.split('.', maxsplit=2)
            if len(splitted_path) == 2:
                app, model_name = splitted_path
                if app in settings.INSTALLED_APPS:
                    app_models = apps.all_models[app]
                    # print(app_models)
                    if model_name.lower() in app_models:
                        if issubclass(app_models[model_name.lower()], BaseModel):
                            app_models[model_name.lower()].all_objects.hard_delete_all()
                        else:
                            app_models[model_name.lower()].objects.all().delete()
                        self.stdout.write("%s deleted" % model_name)
            elif len(splitted_path) == 1:
                app = splitted_path[0]
                if app in settings.INSTALLED_APPS:
                    app_models = apps.all_models[app]
                    for model_name, model_class in app_models.items():
                        if issubclass(model_class, BaseModel):
                            model_class.all_objects.hard_delete_all()
                        else:
                            model_class.objects.all().delete()
                        self.stdout.write("%s deleted" % model_name)
